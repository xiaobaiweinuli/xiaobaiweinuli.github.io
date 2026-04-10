---
title: Cloudflare使用SAAS回源加速
tags:
  - Cloudflare
  - Tunnel
  - SAAS
categories: SAAS回源加速
description: Cloudflare Tunnel 使用SAAS回源加速配置教程
date: 2026-04-11 01:07:53 
---


在使用 Cloudflare Tunnel 时，通过“主域名+加速域名”的联动配置，既能隐藏内网 IP，又能优化访问速度。本文以实际部署场景为例（主域名 `zhuyuming.dpdns.org`、加速域名 `jiasu.dpdns.org`），带你一步步完成内网服务穿透（以 `192.168.1.6:5555` 网页服务为例），实操性强，可直接对照复刻。

## 一、核心信息说明

先明确本次配置的关键信息，后续操作均围绕这些内容展开，替换时直接对应修改即可：

- **主域名**：`zhuyuming.dpdns.org`
- **主域名隧道（实际访问用）**：`panel.zhuyuming.dpdns.org`（用于访问内网 `192.168.1.6:5555` 网页服务）
- **加速域名（转发用）**：`jiasu.dpdns.org`（含两个隧道：
  - `ip.jiasu.dpdns.org`：因内网 IP 无法直接被公网解析，需通过此隧道指向电脑本地 IP `192.168.1.6`；
  - `youxuan.jiasu.dpdns.org`：用于联动加速）
- **内网服务地址**：`192.168.1.6:5555`（需穿透的网页服务）
- **内网设备 IP**：`192.168.1.6`（电脑本地 IP）

## 二、创建隧道（主域名+加速域名）

隧道是 Cloudflare 转发流量的核心，需分别为“主域名”和“加速域名”创建对应隧道。

### 操作路径：

Cloudflare 控制台 → 左侧“Zero Trust” → “Networks” → “Tunnels” → “Create a tunnel”

### 具体操作：

1. **创建主域名隧道（绑定实际访问域名）**
  
  - 隧道名称：`panel-tunnel`
  - 点击“Save tunnel”后，在“Public Hostname”板块点击“Add a public hostname”：
    - **Subdomain**：`panel`（子域名，与主域名组合为 `panel.zhuyuming.dpdns.org`）
    - **Domain**：选择主域名 `zhuyuming.dpdns.org`
    - **Service**：选择“HTTP”，在“Origin”中填写内网服务地址 `192.168.1.6:5555`（关键！隧道会将主域名流量转发到这里）
    - 点击“Save”完成绑定。
2. **创建加速域名隧道（绑定加速子域名）**
  
  - 在同一隧道页面或新建隧道时，点击“Add a public hostname”：
    - **Subdomain**：`ip`（子域名，组合为 `ip.jiasu.dpdns.org`）
    - **Domain**：选择加速域名 `jiasu.dpdns.org`
    - **Service**：选择“HTTP”，“Origin”填写内网设备 IP `192.168.1.6`
    - 点击“Save”完成绑定。

## 三、加速域名配置（jiasu.dpdns.org）

### 1. 为加速域名添加CNAME记录（关闭代理）

通过CNAME记录将加速子域名指向优选源，实现流量优化。

#### 操作路径：

Cloudflare 控制台 → 进入加速域名管理页（`jiasu.dpdns.org`） → “DNS” → “Add record”

#### 具体操作：

- **记录类型**：CNAME
- **Name**：`youxuan`（子域名，完整域名 `youxuan.jiasu.dpdns.org`）
- **Target**：`cloudflare.182682.xyz`（他人提供的CloudFlare优选Cname域名）
- **Proxy status**：关闭（点击橙色云朵变为灰色“DNS only”，避免Cloudflare额外转发）
- 点击“Save”保存。

### 2. 为加速域名设置“回退源”

“回退源”用于隧道转发失败时兜底，确保流量可导向备用地址。

#### 操作路径：

Cloudflare 控制台 → 进入加速域名管理页（`jiasu.dpdns.org`） → “SSL/TLS”

#### 具体操作：

- 在“自定义主机名”配置中，找到“回退源”选项；
- 填写 `ip.jiasu.dpdns.org`（即步骤二创建的加速域名隧道）；
- 点击“Save”生效。

### 3. 设置“自定义主机名”（实际访问域名）

将主域名关联到加速域名的证书与主机配置，确保访问合法性。

#### 操作路径：

Cloudflare 控制台 → 进入加速域名管理页（`jiasu.dpdns.org`） → “SSL/TLS” → “自定义主机名”

#### 具体操作：

- 点击“添加自定义主机名”，输入 `panel.zhuyuming.dpdns.org`（主域名隧道的实际访问域名）；
- 提交后，系统会自动生成“主机名验证TXT记录”和“证书验证TXT记录”（需记录下来，后续在主域名配置中使用）。

## 四、主域名配置（zhuyuming.dpdns.org）

### 1. 添加自定义主机名生成的TXT记录

通过TXT记录完成主域名与加速域名的关联验证。

#### 操作路径：

Cloudflare 控制台 → 进入主域名管理页（`zhuyuming.dpdns.org`） → “DNS” → “Add record”

#### 具体操作：

- 分别添加步骤三第3点生成的两条TXT记录：
  - 第一条（主机名验证）：**Type**选TXT，**Name**填系统提示的子域名（如`_hostname.panel`），**Content**填对应验证值；
  - 第二条（证书验证）：**Type**选TXT，**Name**填系统提示的子域名（如`_acme-challenge.panel`），**Content**填对应验证值；
- 两条记录的“Proxy status”均设为“关闭”，点击“Save”保存。

### 2. 修改主域名隧道指向加速域名（核心转发）

将主域名流量通过隧道转发到加速域名，实现“主域名→加速域名→内网服务”的链路。

#### 操作路径：

Cloudflare 控制台 → 进入主域名管理页（`zhuyuming.dpdns.org`） → “DNS” → 找到`panel`对应的记录 → 点击“Edit”

#### 具体操作：

- 将“Target”修改为加速域名的优选子域名 `youxuan.jiasu.dpdns.org`；
- **Proxy status**：保持“关闭”（灰色云朵）；
- 点击“Save”完成修改。

### 3. 添加自定义主机名的DCV委派

用于SSL证书自动验证，确保证书正常签发。

#### 操作路径：

Cloudflare 控制台 → 进入主域名管理页（`zhuyuming.dpdns.org`） → “DNS” → “Add record”

#### 具体操作：

- **Type**：CNAME
- **Name**：`_acme-challenge`
- **Target**：`zhuyuming.dpdns.org.*6****f***3.dcv.cloudflare.com`（替换为步骤三第3点生成的DCV委派地址）
- **Proxy status**：关闭；
- 点击“Save”保存。

## 总结

本次配置的核心是“主域名→隧道→加速域名→内网服务”的流量链路，关键注意以下3点：

1. **内网IP不可直接解析**：必须通过Cloudflare Tunnel转发，不可仅用DNS指向；
2. **代理状态需关闭**：所有涉及DNS记录和隧道的“Proxy status”均设为“关闭”（灰色云朵），避免转发冲突；
3. **隧道指向需准确**：主域名隧道指向加速域名的优选子域名，加速域名隧道指向内网IP，回退源需关联加速域名隧道。

按此步骤操作，即可用主域名安全访问内网服务，同时借助加速域名优化访问速度。