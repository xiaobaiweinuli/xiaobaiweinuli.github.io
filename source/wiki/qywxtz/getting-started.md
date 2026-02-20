---
wiki: qywxtz
title: 快速开始
---

# 快速开始

本页面将指导您如何快速安装和配置企业微信通知服务。

## 🔧 环境要求

在开始安装之前，请确保您的环境满足以下要求：

- **Node.js**: 18.x 或更高版本 (推荐 18.x LTS)
- **npm**: 8.x 或更高版本
- **Git**: 用于克隆代码仓库
- **企业微信**: 拥有管理员权限，用于创建应用

## 📥 安装方式

### 方式一：克隆代码仓库

```bash
# 克隆代码仓库
git clone https://github.com/xiaobaiweinuli/qywx-push.git

# 进入项目目录
cd qywx-push

# 安装依赖
npm install

# 启动服务
npm start
```

### 方式二：使用Docker部署

```bash
# 拉取镜像
docker pull xiaobaiweinuli/qywx-push:latest

# 运行容器
docker run -d \
  -p 3000:3000 \
  -e PORT=3000 \
  -v ./data:/app/data \
  --name qywx-push \
  xiaobaiweinuli/qywx-push:latest
```

## ⚙️ 配置企业微信

### 1. 创建企业微信应用

1. 登录[企业微信管理后台](https://work.weixin.qq.com/)
2. 进入「应用管理」-「应用」-「自建」
3. 点击「创建应用」
4. 填写应用名称（如：通知服务）和描述
5. 上传应用头像（可选）
6. 点击「创建」完成应用创建

### 2. 获取应用参数

创建应用后，您需要获取以下参数：

- **企业ID (corpid)**: 在「我的企业」-「企业信息」中查看
- **应用Secret (corpsecret)**: 在应用详情页中查看
- **应用ID (agentid)**: 在应用详情页中查看

## 🛠️ 配置服务

### 方式一：环境变量配置

```bash
# Linux/macOS
export CORPID=您的企业ID
export CORPSECRET=您的应用Secret
export AGENTID=您的应用ID
export PORT=3000

# Windows
sets CORPID=您的企业ID
sets CORPSECRET=您的应用Secret
sets AGENTID=您的应用ID
sets PORT=3000
```

### 方式二：配置文件

在项目根目录创建 `.env` 文件：

```env
# 企业微信配置
CORPID=您的企业ID
CORPSECRET=您的应用Secret
AGENTID=您的应用ID

# 服务配置
PORT=3000
HOST=0.0.0.0

# 数据库配置 (SQLite)
DB_PATH=data/db.sqlite

# 安全配置
JWT_SECRET=your_secret_key_here
```

## 🚀 启动服务

### 本地开发环境

```bash
npm run dev
```

### 生产环境

```bash
npm run build
npm start
```

## 🌐 访问管理界面

服务启动后，您可以通过以下地址访问Web管理界面：

```
http://localhost:3000/
```

首次访问时，您需要创建管理员账号。

## 📡 API接口测试

### 发送文本消息

```bash
curl -X POST http://localhost:3000/api/message/text \
  -H "Content-Type: application/json" \
  -d '{
    "touser": "@all",
    "msgtype": "text",
    "text": {
      "content": "测试消息内容"
    }
  }'
```

### 发送Markdown消息

```bash
curl -X POST http://localhost:3000/api/message/markdown \
  -H "Content-Type: application/json" \
  -d '{
    "touser": "@all",
    "msgtype": "markdown",
    "markdown": {
      "content": "# 标题\n## 子标题\n**粗体文本**\n*斜体文本*"
    }
  }'
```

## 🔍 常见问题

### 1. 服务无法启动

- 检查Node.js版本是否符合要求
- 检查端口是否被占用
- 查看日志文件获取详细错误信息

### 2. 无法发送消息

- 确认企业微信参数是否正确
- 检查网络连接是否正常
- 确认应用权限是否设置正确

### 3. 数据库连接失败

- 确认数据库路径是否正确
- 检查文件权限是否足够

## 📚 相关链接

- [高级特性](../advanced/) - 了解更多高级功能
- [部署指南](../deployment/) - 详细的部署说明
- [企业微信API文档](https://developer.work.weixin.qq.com/document/path/90236) - 官方API参考
