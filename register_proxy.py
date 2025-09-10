import requests
from flask import Flask, request, jsonify, redirect
import logging
import json
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建 Flask 应用
app = Flask(__name__)

# MonkeyCode服务配置
MONKEYCODE_BASE_URL = os.getenv('MONKEYCODE_BASE_URL')
LOGIN_URL = f"{MONKEYCODE_BASE_URL}/api/v1/admin/login"
INVITE_URL = f"{MONKEYCODE_BASE_URL}/api/v1/user/invite"

# 登录凭据
LOGIN_CREDENTIALS = {
    "username": os.getenv('MONKEYCODE_USERNAME'),
    "password": os.getenv('MONKEYCODE_PASSWORD'),
    "source": "browser"
}

# Fixed authentication token
AUTH_TOKEN = os.getenv('MONKEYCODE_AUTH_TOKEN')

# Request headers
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
}

@app.route('/register', methods=['GET'])
def get_invite_code():
    """
    Get invitation code interface
    Parameters:
        token: Authentication token
    Returns:
        Invitation code or error message
    """
    try:
        # Get request parameters
        token = request.args.get('token')
        if not token:
            return jsonify({"error": "Missing token parameter"}), 400
        
        # Verify token
        if token != AUTH_TOKEN:
            logger.warning(f"Token verification failed, provided token: {token}")
            return jsonify({"error": "Token verification failed"}), 401
        
        logger.info(f"Received request to get invitation code, token: {token}")
        
        # Step 1: Login to get session
        session = requests.Session()
        login_response = session.post(
            LOGIN_URL,
            headers=HEADERS,
            data=json.dumps(LOGIN_CREDENTIALS),
            verify=False
        )
        
        if login_response.status_code != 200:
            logger.error(f"Login failed, status code: {login_response.status_code}, response: {login_response.text}")
            return jsonify({"error": "Login failed"}), 500
        
        login_data = login_response.json()
        if login_data.get('code') != 0:
            logger.error(f"Login returned error, response: {login_data}")
            return jsonify({"error": "Login failed"}), 500
        
        logger.info("Login successful")
        
        # Step 2: Get invitation code
        invite_headers = HEADERS.copy()
        invite_headers['Referer'] = f"{MONKEYCODE_BASE_URL}/member-management"
        
        invite_response = session.get(
            INVITE_URL,
            headers=invite_headers,
            verify=False
        )
        
        if invite_response.status_code != 200:
            logger.error(f"Failed to get invitation code, status code: {invite_response.status_code}, response: {invite_response.text}")
            return jsonify({"error": "Failed to get invitation code"}), 500
        
        invite_data = invite_response.json()
        if invite_data.get('code') != 0:
            logger.error(f"Getting invitation code returned error, response: {invite_data}")
            return jsonify({"error": "Failed to get invitation code"}), 500
        
        # Extract invitation code
        invite_code = invite_data.get('data', {}).get('code')
        if not invite_code:
            logger.error(f"Invitation code format error, response: {invite_data}")
            return jsonify({"error": "Invitation code format error"}), 50
        
        logger.info(f"Successfully obtained invitation code: {invite_code}")
        
        # Construct the redirect URL
        redirect_url = f"{MONKEYCODE_BASE_URL}/invite/{invite_code}/1"
        
        # Perform redirect
        return redirect(redirect_url)
    
    except Exception as e:
        logger.error(f"Exception occurred while processing request: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # 禁用 SSL 警告
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    
    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=82, debug=True)