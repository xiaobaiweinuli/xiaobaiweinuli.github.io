---
wiki: qywxtz
title: 高级特性
---

# 高级特性

本章介绍企业微信通知服务的高级功能和配置选项，帮助您充分利用系统的强大功能。

## 🔄 多应用管理

企业微信通知服务支持同时管理多个企业微信应用，每个应用可以有独立的配置。

### 添加新应用

1. 登录Web管理界面
2. 进入「应用管理」-「添加应用」
3. 填写应用名称和企业微信参数
4. 点击「保存」完成添加

### 应用切换

在发送消息时，可以通过指定应用ID来选择使用哪个应用发送消息：

```bash
curl -X POST http://localhost:3000/api/message/text \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "your_app_identifier",
    "touser": "@all",
    "msgtype": "text",
    "text": {
      "content": "来自特定应用的消息"
    }
  }'
```

## 📊 消息模板

为了方便重复使用相似的消息格式，系统提供了消息模板功能。

### 创建消息模板

1. 进入「模板管理」-「创建模板」
2. 选择消息类型
3. 填写模板名称和内容
4. 使用 `{{变量名}}` 定义可替换的变量
5. 点击「保存」完成创建

### 使用模板发送消息

```bash
curl -X POST http://localhost:3000/api/message/template \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "your_template_id",
    "touser": "@all",
    "data": {
      "username": "张三",
      "action": "登录",
      "time": "2024-01-01 12:00:00"
    }
  }'
```

## 🔐 安全配置

### JWT认证

为了保护API接口安全，系统支持JWT（JSON Web Token）认证。

#### 生成访问令牌

```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'
```

#### 使用令牌访问API

```bash
curl -X POST http://localhost:3000/api/message/text \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_jwt_token" \
  -d '{
    "touser": "@all",
    "msgtype": "text",
    "text": {
      "content": "受保护的API调用"
    }
  }'
```

## 🔄 回调配置

企业微信通知服务支持企业微信回调，可以接收用户发送的消息。

### 配置回调URL

1. 在企业微信管理后台，进入应用详情页
2. 找到「开发者接口」-「设置API接收消息」
3. 填写回调URL：`http://your-server.com/api/callback`
4. 生成并填写Token和EncodingAESKey
5. 在配置文件中配置相同的Token和EncodingAESKey

### 回调消息处理

当接收到回调消息时，系统会自动处理并存储。您可以通过API获取回调消息记录。

## 🔌 插件系统

企业微信通知服务支持插件扩展，可以通过插件实现自定义功能。

## 📚 相关链接

- [快速开始](../getting-started/) - 基础安装和配置
- [部署指南](../deployment/) - 部署最佳实践

