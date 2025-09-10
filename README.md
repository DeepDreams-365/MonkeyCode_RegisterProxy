# MonkeyCode 注册代理服务

## 项目简介

MonkeyCode 注册代理服务是一个基于 Flask 的轻量级代理应用，用于生成 MonkeyCode 平台的注册邀请链接。该服务通过代理方式连接到 MonkeyCode 后台管理系统，自动获取邀请码并重定向用户到注册页面。

## 功能说明

- 接收带有认证 token 的注册请求
- 验证请求的合法性
- 登录到 MonkeyCode 后台管理系统
- 获取邀请码
- 重定向用户到注册页面

## 环境变量配置

在运行服务之前，需要配置以下环境变量：

| 环境变量名                | 说明                              | 示例值                              |
| ------------------------- | --------------------------------- | ----------------------------------- |
| `MONKEYCODE_BASE_URL`   | MonkeyCode 后台管理系统的基础 URL | `请替换为实际的MonkeyCode后台URL` |
| `MONKEYCODE_USERNAME`   | 后台管理系统的登录用户名          | `admin`                           |
| `MONKEYCODE_PASSWORD`   | 后台管理系统的登录密码            | `请替换为实际的密码`              |
| `MONKEYCODE_AUTH_TOKEN` | 服务访问认证 token                | `请替换为自定义的认证token`       |
| `FLASK_ENV`             | Flask 运行环境                    | `production`                      |

## 部署方式

### 使用 Docker Compose 部署（推荐）

1. 确保已安装 Docker 和 Docker Compose
2. 打包镜像：`docker build -t monkeycode-register-proxy:latest .`
3. 修改 `docker-compose.yaml` 文件中的环境变量配置
4. 运行以下命令启动服务：

```bash
docker-compose up -d
```

### 直接运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 设置环境变量：

```bash
export MONKEYCODE_BASE_URL=请替换为实际的MonkeyCode后台URL
export MONKEYCODE_USERNAME=admin
export MONKEYCODE_PASSWORD=请替换为实际的密码
export MONKEYCODE_AUTH_TOKEN=请替换为自定义的认证token
```

3. 运行应用：

```bash
python register_proxy.py
```

## 使用方法

服务启动后，默认监听 82 端口。通过以下方式获取注册邀请链接：

```
GET http://<server-ip>:82/register?token=<MONKEYCODE_AUTH_TOKEN>
```

例如：

```
GET http://localhost:82/register?token=请替换为自定义的认证token
```

如果 token 验证通过，服务将自动获取邀请码并重定向到 MonkeyCode 注册页面。

## 注意事项

1. 请确保 MonkeyCode 后台管理系统的 URL、用户名和密码配置正确
2. 为了安全起见，建议定期更换 `MONKEYCODE_AUTH_TOKEN`
3. 在生产环境中，请使用 HTTPS 来保护传输安全
4. 服务默认以 debug 模式运行，生产环境中应考虑关闭 debug 模式
