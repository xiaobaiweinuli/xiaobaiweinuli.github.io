---
title: GitHub / Cloudflare API 文档与 Schema 获取指南
tags:
  - GitHub
  - Cloudflare
  - REST API
  - GraphQL API
categories: API
description: 本文整理了 GitHub 和 Cloudflare 两家平台的 GraphQL / REST API，各自官方提供的完整接口文档、Schema 获取方式，便于开发时查阅和二次开发（生成 SDK、导入 Postman 等）。
date: 2026-07-16 10:20:57
---
# GitHub / Cloudflare API 文档与 Schema 获取指南

本文整理了 GitHub 和 Cloudflare 两家平台的 GraphQL / REST API，各自官方提供的完整接口文档、Schema 获取方式，便于开发时查阅和二次开发（生成 SDK、导入 Postman 等）。

## 目录

- [一、GitHub GraphQL API](#一github-graphql-api)
- [二、GitHub REST API](#二github-rest-api)
- [三、Cloudflare GraphQL Analytics API](#三cloudflare-graphql-analytics-api)
- [四、Cloudflare REST API（v4）](#四cloudflare-rest-apiv4)
- [五、拿到 Schema 之后能做什么](#五拿到-schema-之后能做什么)

---

## 一、GitHub GraphQL API

GitHub 的 GraphQL API 支持 query 和 mutation（可读可写），官方提供三种获取完整 Schema 的方式。

### 1.1 官方文档站（网页浏览，适合人工查阅）

**入口**：https://docs.github.com/en/graphql/reference

按类型分类，每类一个子页面：

| 分类 | 链接 |
|---|---|
| Objects（对象类型） | https://docs.github.com/en/graphql/reference/objects |
| Queries（查询根字段） | https://docs.github.com/en/graphql/reference/queries |
| Mutations（可写操作） | https://docs.github.com/en/graphql/reference/mutations |
| Interfaces / Unions / Enums / Input Objects / Scalars | 各有独立页面，在同一 reference 目录下 |

### 1.2 官方仓库中的原始 Schema 文件（机器可读，最权威）

**仓库**：https://github.com/github/docs

**路径**：`src/graphql/data/fpt/schema.docs.graphql`

标准 `.graphql` / SDL 格式纯文本，可直接下载、全文搜索，或喂给 GraphQL Code Generator 等代码生成工具。

### 1.3 自己发起 Introspection 查询（最实时，不依赖文档滞后）

**官方出处**：https://docs.github.com/en/graphql/guides/introduction-to-graphql （"Discovering the GraphQL API" 一节）——以下三种方式均来自该页面的官方原文。

#### 方式一：简化版查询（仅取类型名、kind、描述、字段名）

官方文档给出的最简 introspection 查询，适合快速浏览有哪些类型、不需要参数细节时使用：

```bash
curl -X POST https://api.github.com/graphql \
  -H "Authorization: bearer <<GITHUB_TOKEN>>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { __schema { types { name kind description fields { name } } } }"
  }'
```

也可以针对单个类型查询（比如只想看 `Repository` 类型有哪些基础字段）：

```graphql
query {
  __type(name: "Repository") {
    name
    kind
    description
    fields {
      name
    }
  }
}
```

如果要查的是某个 **mutation 输入类型的参数**（即 `inputFields`，而不是普通对象类型的 `fields`），用法类似。这里以 `CreateUserListInput`（创建星标分类清单的输入类型）为例：

```graphql
query {
  __type(name: "CreateUserListInput") {
    inputFields {
      name
      type {
        name
        kind
        ofType {
          name
          kind
        }
      }
    }
  }
}
```

需要注意 **`__Type.inputFields` 元字段单次请求最多只能出现 2 次**（GitHub 的 introspection 限流规则），超过会报错：

```json
{
  "errors": [
    {
      "type": "INTROSPECTION_LIMIT_EXCEEDED",
      "message": "Introspection fields may only be used 2 times, but some fields were used more than that: __Type.inputFields (4)"
    }
  ]
}
```

需要一次查多个类型的 `inputFields` 时，拆成多次请求，每次不超过 2 个，用别名区分（这里以 `CreateUserListInput` 和 `UpdateUserListInput` 为例）：

```bash
curl -X POST https://api.github.com/graphql \
  -H "Authorization: bearer <<GITHUB_TOKEN>>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { createList: __type(name: \"CreateUserListInput\") { inputFields { name type { name kind ofType { name kind } } } } updateList: __type(name: \"UpdateUserListInput\") { inputFields { name type { name kind ofType { name kind } } } } }"
  }'
```

#### 方式二：标准 JSON Introspection Query

如果需要 JSON 格式（例如用代码处理），使用 GraphQL 社区通用的完整 introspection query。该查询用 fragment 复用重复结构，`fields`/`inputFields` 等元字段在查询文本中只出现一次，不会触发"字段调用次数超限"的限流。

```bash
curl -X POST https://api.github.com/graphql \
  -H "Authorization: bearer <<GITHUB_TOKEN>>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description locations args { ...InputValue } } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }"
  }' -o github_schema_full.json
```

> **注意**：该查询返回的 JSON 会比"仅取字段名"的简化版本大得多（因为附带了每个字段的完整参数列表与类型链），实际体积可达数 MB 级别，建议直接存文件而非打印到终端。

#### 方式三：一次 GET 拿精简版 SDL 文本

GitHub 支持通过特殊 `Accept` 头，返回**精简版**（condensed version）的 SDL（Schema Definition Language）纯文本，无需走标准 introspection query，也不会触发字段调用次数限制。官方原文的表述是 "a condensed version of the schema"（schema 的精简版），并非完整详尽版本：

```bash
curl -H "Authorization: bearer <<GITHUB_TOKEN>>" \
     -H "Accept: application/vnd.github.v4.idl" \
     https://api.github.com/graphql
```

**补充**：不加 `Accept` 头、直接对同一端点发 `GET` 请求（而非 `POST`），也能拿到 JSON 格式的 introspection 结果，这是官方文档里提到的另一种写法：

```bash
curl -H "Authorization: bearer <<GITHUB_TOKEN>>" https://api.github.com/graphql
```

官方文档同时给出了排查提示：如果遇到 `"message": "Bad credentials"` 或 `401 Unauthorized`，检查 token 是否有效；如果遇到 `403` 且提示 `Resource not accessible by personal access token`，需确认 Fine-grained token 的 Resource owner 指向了正确的组织/账号（比如目标仓库所属的组织）。

返回内容示例（以 `Repository` 类型和 `UpdateUserListsForItemInput` 为例）：

```graphql
type Repository implements Node & PackageOwner & ProjectOwner & Starrable {
  id: ID!
  name: String!
  stargazerCount: Int!
  issues(states: [IssueState!], first: Int, after: String): IssueConnection!
  ...
}

input UpdateUserListsForItemInput {
  itemId: ID!
  listIds: [ID!]!
  suggestedListIds: [ID!]
  clientMutationId: String
}
```

所有字段的参数、input 类型字段、枚举取值均已完整展开，无需再逐个 `__type(name: "...")` 单独查询。



---

## 二、GitHub REST API

GitHub REST API 由官方维护的 **OpenAPI 3.0 / 3.1 规范**完整描述，用于自动生成官方文档和 Octokit 系列 SDK。

**官方仓库**：https://github.com/github/rest-api-description

### 下载最新版本

```bash
# 3.1 版本，bundled（打包）格式，最常用
curl -L "https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json" \
  -o github_rest_openapi.json
```

### 说明

| 目录 | 含义 |
|---|---|
| `descriptions/` | OpenAPI 3.0 版本 |
| `descriptions-next/` | OpenAPI 3.1 版本（仍在演进，主分支可能有破坏性变更） |

每个产品线单独维护一份文件：

- `api.github.com` — GitHub Free / Pro / Team
- `ghec` — GitHub Enterprise Cloud
- `ghes-X.X` — 各版本 GitHub Enterprise Server（自托管）

每份规范提供两种格式：

- **bundled**（打包）：保留 `$ref` 引用，文件较小
- **dereferenced**（完全展开，文件名含 `.deref.json`）：无引用，更直观但体积更大

规范中包含每个接口的完整请求参数、响应结构、错误码定义，可靠性优于手工试错拼接请求。

---

## 三、Cloudflare GraphQL Analytics API

Cloudflare 的 GraphQL API 专用于**只读分析数据查询**（不含 mutation），覆盖几乎全部产品线的用量与性能指标。

### 3.1 官方参考资料

**Cloudflare 官方 Skills 仓库**：
https://github.com/cloudflare/skills/tree/main/skills/cloudflare/references/graphql-api

该仓库由 Cloudflare 官方维护，用于指导 AI Agent / 开发者使用其产品，核心信息如下：

- 单一端点：`https://api.cloudflare.com/client/v4/graphql`
- 覆盖 **1400+ 个 Schema 类型**，涵盖几乎所有 Cloudflare 产品线
- 两种作用域：**zone-level**（按域名）与 **account-level**（跨域名，账号级）
- 高流量数据集使用**自适应采样**（Adaptive sampling），并带置信区间
- **纯只读**，无 mutation（Mutation 类型为空壳）
- 速率限制：默认每用户每 5 分钟 300 次查询（上限 320，具体消耗取决于查询复杂度）

### 3.2 第三方整理的字段文档（非官方，内容详尽）

https://pages.johnspurlock.com/graphql-schema-docs/cloudflare.html

基于官方 Schema introspection 导出的静态 HTML 文档，字段覆盖面比官方文档更全（含 Calls SFU 带宽、Cloudchamber 指标、Shadow IT 分析、Sinkhole 请求日志、Turnstile 事件等冷门数据集），适合直接搜索字段名。内容来源于官方 Schema，可信度较高，但不保证与最新版本同步。

### 3.3 自行 Introspection（最实时，权限范围内数据最准确）

**官方出处**：https://developers.cloudflare.com/analytics/graphql-api/features/discovery/introspection/ ——该页面标题为 "Introspection"，明确说明 Cloudflare GraphQL API 暴露 70+ 个数据集，且动态变化，官方建议用 `__schema` 节点做 introspection 来发现最新可用字段。以下"方式二"的完整版查询是该页面原文给出的示例（标注为 "A typical introspection query"），并非社区通用版本套用，是 Cloudflare 官方文档原文。

#### 方式一：简化版查询（仅取类型和字段名）

```bash
curl -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name fields { name } } } } "}'
```

#### 方式二：标准 JSON Introspection Query（含参数、输入字段、枚举值等全部细节）

```bash
curl -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query IntrospectionQuery { __schema { queryType { name } mutationType { name } subscriptionType { name } types { ...FullType } directives { name description locations args { ...InputValue } } } } fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces { ...TypeRef } enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason } possibleTypes { ...TypeRef } } fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }"
  }' -o cloudflare_schema_full.json
```

### 3.4 使用须知

1. **鉴权方式**：使用 `Authorization: Bearer $API_TOKEN`（Cloudflare **API Token**），需在 Dashboard 生成带 `Account Analytics` 读权限的 Token；这与 OAuth Client Token 是两套不同的鉴权体系。
2. **数据体量较大**：完整 introspection 结果预计与 GitHub 完整版（约 5.9MB）同量级或更大，建议直接存文件而非终端打印。
3. **无简化 IDL 端点**：Cloudflare 目前未提供类似 GitHub `Accept: application/vnd.github.v4.idl` 的一键 SDL 文本获取方式，仅能通过标准 introspection query 获取。
4. **Schema 是动态变化的**：官方原文提到 Cloudflare GraphQL API 暴露 70+ 个数据集，且持续新增、替换。字段描述里会标注是否处于 **Beta 模式**（面向更高套餐用户测试，随时可能变更或下线，不建议长期依赖）以及**弃用状态**（如果有 sunset 日期，需在此日期前迁移到替代节点）。
5. **官方在线 GraphQL Explorer**：https://graphql.cloudflare.com/explorer ——可以直接在浏览器里跑 introspection 查询和调试，不用本地起 GraphiQL/Altair 客户端。
6. **官方 curl 使用指南**：https://developers.cloudflare.com/analytics/graphql-api/getting-started/execute-graphql-query/ ——讲解如何用 curl 正确发送 GraphQL 请求（鉴权头、请求体格式等）。

---

## 四、Cloudflare REST API（v4）

Cloudflare REST API v4 同样提供官方 OpenAPI 规范。

```bash
curl -L "https://raw.githubusercontent.com/cloudflare/api-schemas/main/openapi.json"
```

> 若上述具体路径失效，请直接访问仓库首页确认最新文件路径：
> https://github.com/cloudflare/api-schemas

---

## 五、拿到 Schema 之后能做什么

- **导入 Postman / Insomnia**：自动渲染为可交互的接口浏览器，包含参数说明与鉴权配置，无需手动拼接请求
- **生成客户端 SDK**：配合 `openapi-generator`（REST）或 GraphQL Code Generator（GraphQL）等工具，自动生成对应语言的强类型客户端代码
- **接口校验**：对照官方 Schema 校验自己手写的请求体是否使用了不存在的字段，避免线上报错
- **区分公开 API 与内部专属字段**：部分从浏览器抓包获得的请求可能包含仅供官方前端使用、未出现在公开 Schema 中的字段（例如 GitHub 网页版内部查询），对照公开 Schema 逐字段核对可以快速识别这类差异