---
wiki: qywxtz
title: 部署指南
---

# 部署指南

本页面提供企业微信通知服务的详细部署步骤和最佳实践，帮助您在生产环境中稳定运行服务。

## 🐳 Docker部署（推荐）

### 基础部署

```bash
# 拉取最新镜像
docker pull xiaobaiweinuli/qywx-push:latest

# 运行容器
docker run -d \
  -p 3000:3000 \
  -e PORT=3000 \
  -v ./data:/app/data \
  --name qywx-push \
  xiaobaiweinuli/qywx-push:latest
```

### 使用Docker Compose

创建 `docker-compose.yml` 文件：

```yaml
services:
  qywx-push:
    image: xiaobaiweinuli/qywx-push:latest
    container_name: qywx-push
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
    environment:
      - PORT=3000
      - HOST=0.0.0.0
      - CORPID=your_corpid
      - CORPSECRET=your_corpsecret
      - AGENTID=your_agentid
      - DB_PATH=/app/data/db.sqlite
    restart: unless-stopped
```

启动服务：

```bash
docker-compose up -d
```

## 🖥️ 本地服务器部署

### 环境准备

```bash
# 安装Node.js和npm（Ubuntu示例）
sudo apt update
sudo apt install -y nodejs npm

# 升级npm
npm install -g npm
```

### 安装服务

```bash
# 克隆代码
git clone https://github.com/xiaobaiweinuli/qywx-push.git
cd qywx-push

# 安装依赖
npm install

# 构建生产版本
npm run build
```

### 使用PM2管理进程

```bash
# 安装PM2
npm install -g pm2

# 启动服务
pm run build
pm start

# 或者使用PM2直接管理
pm run build
pm start
```

## 🌐 反向代理配置

### Nginx配置示例

```nginx
server {
    listen 80;
    server_name notification.yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### HTTPS配置

使用Let's Encrypt配置SSL证书：

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 生成SSL证书
sudo certbot --nginx -d notification.yourdomain.com
```

## 🔧 环境变量完整列表

```env
# 基本配置
PORT=3000
HOST=0.0.0.0
NODE_ENV=production

# 企业微信配置
CORPID=your_corpid
CORPSECRET=your_corpsecret
AGENTID=your_agentid

# 数据库配置
DB_PATH=data/db.sqlite

# 安全配置
JWT_SECRET=your_jwt_secret_key
ENABLE_IP_WHITELIST=false
IP_WHITELIST=127.0.0.1

# 回调配置
CALLBACK_TOKEN=your_callback_token
CALLBACK_AES_KEY=your_callback_aes_key

# 文件上传配置
MAX_FILE_SIZE=10485760
UPLOAD_PATH=uploads

# 日志配置
LOG_LEVEL=info
LOG_FILE=logs/app.log
```

## 📊 监控与日志

### 日志查看

```bash
# Docker日志
docker logs qywx-push

# 本地服务日志
cat logs/app.log
```

### 健康检查

系统提供了健康检查接口，可以用于监控服务状态：

```bash
curl http://localhost:3000/api/health
```

## 🛡️ 安全建议

1. **使用HTTPS** - 确保所有请求使用HTTPS加密传输
2. **设置强密码** - 为管理员账号设置复杂密码
3. **配置IP白名单** - 限制只有特定IP可以访问管理接口
4. **定期备份数据** - 定期备份数据库文件
5. **保持更新** - 及时更新到最新版本获取安全补丁

## 📚 相关链接

- [快速开始](../getting-started/) - 基础安装和配置
- [高级特性](../advanced/) - 高级功能说明

## 完成后的Wiki结构

完成以上所有文件的创建和修改后，您的Wiki结构如下：

```
d:\15268\Desktop\blog\source\_
├── data\
│   ├── wiki\
│   │   └── qywxtz.yml  # 项目配置文件（已更新）
│   └── wiki.yml        # Wiki上架配置（已确认包含qywxtz）
└── wiki\
    └── qywxtz\
        ├── index.md           # 项目首页（已更新）
        ├── getting-started.md # 快速开始（已更新）
        ├── advanced.md        # 高级特性（新建）
        └── deployment.md      # 部署指南（新建）
```