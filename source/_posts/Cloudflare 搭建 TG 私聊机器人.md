---
title: 'Cloudflare 搭建 TG 私聊机器人'
date: '2023-12-16 23:01:42'
tags: ['CloudFlare']
categories: ['默认分类']
description: ''
toc: 'True'
---
**源码**：[LloydAsp/nfd: No Fraud / Node Forward Bot](https://github.com/LloydAsp/nfd)

### 特点

- 基于 Workers 搭建，只要你的配额够，CF 不拉闸，那么就不存在跑路的问题。
- 0 成本，连域名都不需要。
- 接入反欺诈系统，当聊天对象有诈骗历史时，自动发出提醒。
- 支持屏蔽用户，避免被骚扰。

## 搭建方法

首先去 [`@BotFather`](https://t.me/BotFather) 创建一个新机器人，获取一个 API KEY（`Token`）。
然后使用 `/setjoingroups` 命令禁止机器人被添加到群组。
找一个获取 [`UUID`](https://www.uuidgenerator.net) 的网站，随机获取一个 UUID。
使用 [`@userinfobot` ]( https://t.me/userinfobot ) 获取你的 TGID（或者 username_to_id_bot）。
然后前往 [`Cloudflare`](https://dash.cloudflare.com) 控制台，创建一个示例 Workers。
然后在设置中添加环境变量。

- `ENV_BOT_TOKEN` 变量，值为 Bot 的 Token
- `ENV_BOT_SECRET` 变量，值为 UUID
- `ENV_ADMIN_UID` 变量，值为 TGID

新建一个名字叫做 `nfd` 的 KV 数据库然后绑定 nfd = nfd。
回到上面，快速编辑里面编辑代码。

### 代码一

将 [`本文件`](https://github.com/LloydAsp/nfd/blob/main/worker.js) 内容全部复制即可。
修改后保存并部署即可。
然后访问 `https://demoworkers.dev/registerWebhook` 注册 WebSoket 即可。
**使用方法**
- 当其他用户给 bot 发消息，会被转发到 bot 创建者
- 用户回复普通文字给转发的消息时，会回复到原消息发送者
- 用户回复/block, /unblock, /checkblock 等命令会执行相关指令，不会回复到原消息发送者

### 代码二

```javascript
 <span role="presentation">const TOKEN = ENV_BOT_TOKEN // Get it from @BotFather</span>
 <span role="presentation">const WEBHOOK = '/endpoint'</span>
 <span role="presentation">const SECRET = ENV_BOT_SECRET // A-Z, a-z, 0-9, _ and -</span>
 <span role="presentation">const ADMIN_UID = ENV_ADMIN_UID // your user id, get it from https://t.me/username_to_id_bot</span>
 <span role="presentation">​</span>
 <span role="presentation">const NOTIFY_INTERVAL = 3600 * 1000;</span>
 <span role="presentation">const fraudDb = 'https://raw.githubusercontent.com/LloydAsp/nfd/main/data/fraud.db';</span>
 <span role="presentation">const notificationUrl = 'https://raw.githubusercontent.com/LloydAsp/nfd/main/data/notification.txt'</span>
 <span role="presentation">const startMsgUrl = 'https://raw.githubusercontent.com/LloydAsp/nfd/main/data/startMessage.md';</span>
 <span role="presentation">​</span>
 <span role="presentation">const enable_notification = true</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Return url to telegram api, optionally with parameters added</span>
 <span role="presentation"> */</span>
 <span role="presentation">function apiUrl (methodName, params = null) {</span>
 <span role="presentation">  let query = ''</span>
 <span role="presentation">  if (params) {</span>
 <span role="presentation">    query = '?' + new URLSearchParams(params).toString()</span>
 <span role="presentation">  }</span>
 <span role="presentation">  return `https://api.telegram.org/bot${TOKEN}/${methodName}${query}`</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">function requestTelegram(methodName, body, params = null){</span>
 <span role="presentation">  return fetch(apiUrl(methodName, params), body)</span>
 <span role="presentation">    .then(r => r.json())</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">function makeReqBody(body){</span>
 <span role="presentation">  return {</span>
 <span role="presentation">    method:'POST',</span>
 <span role="presentation">    headers:{</span>
 <span role="presentation">      'content-type':'application/json'</span>
 <span role="presentation">    },</span>
 <span role="presentation">    body:JSON.stringify(body)</span>
 <span role="presentation">  }</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">function sendMessage(msg = {}){</span>
 <span role="presentation">  return requestTelegram('sendMessage', makeReqBody(msg))</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">function copyMessage(msg = {}){</span>
 <span role="presentation">  return requestTelegram('copyMessage', makeReqBody(msg))</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">function forwardMessage(msg){</span>
 <span role="presentation">  return requestTelegram('forwardMessage', makeReqBody(msg))</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Wait for requests to the worker</span>
 <span role="presentation"> */</span>
 <span role="presentation">addEventListener('fetch', event => {</span>
 <span role="presentation">  const url = new URL(event.request.url)</span>
 <span role="presentation">  if (url.pathname === WEBHOOK) {</span>
 <span role="presentation">    event.respondWith(handleWebhook(event))</span>
 <span role="presentation">  } else if (url.pathname === '/registerWebhook') {</span>
 <span role="presentation">    event.respondWith(registerWebhook(event, url, WEBHOOK, SECRET))</span>
 <span role="presentation">  } else if (url.pathname === '/unRegisterWebhook') {</span>
 <span role="presentation">    event.respondWith(unRegisterWebhook(event))</span>
 <span role="presentation">  } else {</span>
 <span role="presentation">    event.respondWith(new Response('No handler for this request'))</span>
 <span role="presentation">  }</span>
 <span role="presentation">})</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Handle requests to WEBHOOK</span>
 <span role="presentation"> * https://core.telegram.org/bots/api#update</span>
 <span role="presentation"> */</span>
 <span role="presentation">async function handleWebhook (event) {</span>
 <span role="presentation">  // Check secret</span>
 <span role="presentation">  if (event.request.headers.get('X-Telegram-Bot-Api-Secret-Token') !== SECRET) {</span>
 <span role="presentation">    return new Response('Unauthorized', { status: 403 })</span>
 <span role="presentation">  }</span>
 <span role="presentation">​</span>
 <span role="presentation">  // Read request body synchronously</span>
 <span role="presentation">  const update = await event.request.json()</span>
 <span role="presentation">  // Deal with response asynchronously</span>
 <span role="presentation">  event.waitUntil(onUpdate(update))</span>
 <span role="presentation">​</span>
 <span role="presentation">  return new Response('Ok')</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Handle incoming Update</span>
 <span role="presentation"> * https://core.telegram.org/bots/api#update</span>
 <span role="presentation"> */</span>
 <span role="presentation">async function onUpdate (update) {</span>
 <span role="presentation">  if ('message' in update) {</span>
 <span role="presentation">    await onMessage(update.message)</span>
 <span role="presentation">  }</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Handle incoming Message</span>
 <span role="presentation"> * https://core.telegram.org/bots/api#message</span>
 <span role="presentation"> */</span>
 <span role="presentation">async function onMessage (message) {</span>
 <span role="presentation">  if(message.text === '/start'){</span>
 <span role="presentation">    let startMsg = await fetch(startMsgUrl).then(r => r.text())</span>
 <span role="presentation">    return sendMessage({</span>
 <span role="presentation">      chat_id:message.chat.id,</span>
 <span role="presentation">      text:startMsg,</span>
 <span role="presentation">    })</span>
 <span role="presentation">  }</span>
 <span role="presentation">  if(message.chat.id.toString() === ADMIN_UID){</span>
 <span role="presentation">    if(!message?.reply_to_message?.chat){</span>
 <span role="presentation">      return sendMessage({</span>
 <span role="presentation">        chat_id:ADMIN_UID,</span>
 <span role="presentation">        text:'使用方法，回复转发的消息，并发送回复消息，或者`/block`、`/unblock`、`/checkblock`等指令'</span>
 <span role="presentation">      })</span>
 <span role="presentation">    }</span>
 <span role="presentation">    if(/^\/block$/.exec(message.text)){</span>
 <span role="presentation">      return handleBlock(message)</span>
 <span role="presentation">    }</span>
 <span role="presentation">    if(/^\/unblock$/.exec(message.text)){</span>
 <span role="presentation">      return handleUnBlock(message)</span>
 <span role="presentation">    }</span>
 <span role="presentation">    if(/^\/checkblock$/.exec(message.text)){</span>
 <span role="presentation">      return checkBlock(message)</span>
 <span role="presentation">    }</span>
 <span role="presentation">    let guestChantId = await nfd.get('msg-map-' + message?.reply_to_message.message_id,</span>
 <span role="presentation">                                      { type: "json" })</span>
 <span role="presentation">    return copyMessage({</span>
 <span role="presentation">      chat_id: guestChantId,</span>
 <span role="presentation">      from_chat_id:message.chat.id,</span>
 <span role="presentation">      message_id:message.message_id,</span>
 <span role="presentation">    })</span>
 <span role="presentation">  }</span>
 <span role="presentation">  return handleGuestMessage(message)</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">async function handleGuestMessage(message){</span>
 <span role="presentation">  let chatId = message.chat.id;</span>
 <span role="presentation">  let isblocked = await nfd.get('isblocked-' + chatId, { type: "json" })</span>
 <span role="presentation">  </span>
 <span role="presentation">  if(isblocked){</span>
 <span role="presentation">    return sendMessage({</span>
 <span role="presentation">      chat_id: chatId,</span>
 <span role="presentation">      text:'Your are blocked'</span>
 <span role="presentation">    })</span>
 <span role="presentation">  }</span>
 <span role="presentation">​</span>
 <span role="presentation">  let forwardReq = await forwardMessage({</span>
 <span role="presentation">    chat_id:ADMIN_UID,</span>
 <span role="presentation">    from_chat_id:message.chat.id,</span>
 <span role="presentation">    message_id:message.message_id</span>
 <span role="presentation">  })</span>
 <span role="presentation">  console.log(JSON.stringify(forwardReq))</span>
 <span role="presentation">  if(forwardReq.ok){</span>
 <span role="presentation">    await nfd.put('msg-map-' + forwardReq.result.message_id, chatId)</span>
 <span role="presentation">  }</span>
 <span role="presentation">  return handleNotify(message)</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">async function handleNotify(message){</span>
 <span role="presentation">  // 先判断是否是诈骗人员，如果是，则直接提醒</span>
 <span role="presentation">  // 如果不是，则根据时间间隔提醒：用户id，交易注意点等</span>
 <span role="presentation">  let chatId = message.chat.id;</span>
 <span role="presentation">  if(await isFraud(chatId)){</span>
 <span role="presentation">    return sendMessage({</span>
 <span role="presentation">      chat_id: ADMIN_UID,</span>
 <span role="presentation">      text:`检测到骗子，UID${chatId}`</span>
 <span role="presentation">    })</span>
 <span role="presentation">  }</span>
 <span role="presentation">  if(enable_notification){</span>
 <span role="presentation">    let lastMsgTime = await nfd.get('lastmsg-' + chatId, { type: "json" })</span>
 <span role="presentation">    if(!lastMsgTime || Date.now() - lastMsgTime > NOTIFY_INTERVAL){</span>
 <span role="presentation">      await nfd.put('lastmsg-' + chatId, Date.now())</span>
 <span role="presentation">      return sendMessage({</span>
 <span role="presentation">        chat_id: ADMIN_UID,</span>
 <span role="presentation">        text:await fetch(notificationUrl).then(r => r.text())</span>
 <span role="presentation">      })</span>
 <span role="presentation">    }</span>
 <span role="presentation">  }</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">async function handleBlock(message){</span>
 <span role="presentation">  let guestChantId = await nfd.get('msg-map-' + message.reply_to_message.message_id,</span>
 <span role="presentation">                                      { type: "json" })</span>
 <span role="presentation">  if(guestChantId === ADMIN_UID){</span>
 <span role="presentation">    return sendMessage({</span>
 <span role="presentation">      chat_id: ADMIN_UID,</span>
 <span role="presentation">      text:'不能屏蔽自己'</span>
 <span role="presentation">    })</span>
 <span role="presentation">  }</span>
 <span role="presentation">  await nfd.put('isblocked-' + guestChantId, true)</span>
 <span role="presentation">​</span>
 <span role="presentation">  return sendMessage({</span>
 <span role="presentation">    chat_id: ADMIN_UID,</span>
 <span role="presentation">    text: `UID:${guestChantId}屏蔽成功`,</span>
 <span role="presentation">  })</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">async function handleUnBlock(message){</span>
 <span role="presentation">  let guestChantId = await nfd.get('msg-map-' + message.reply_to_message.message_id,</span>
 <span role="presentation">  { type: "json" })</span>
 <span role="presentation">​</span>
 <span role="presentation">  await nfd.put('isblocked-' + guestChantId, false)</span>
 <span role="presentation">​</span>
 <span role="presentation">  return sendMessage({</span>
 <span role="presentation">    chat_id: ADMIN_UID,</span>
 <span role="presentation">    text:`UID:${guestChantId}解除屏蔽成功`,</span>
 <span role="presentation">  })</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">async function checkBlock(message){</span>
 <span role="presentation">  let guestChantId = await nfd.get('msg-map-' + message.reply_to_message.message_id,</span>
 <span role="presentation">  { type: "json" })</span>
 <span role="presentation">  let blocked = await nfd.get('isblocked-' + guestChantId, { type: "json" })</span>
 <span role="presentation">​</span>
 <span role="presentation">  return sendMessage({</span>
 <span role="presentation">    chat_id: ADMIN_UID,</span>
 <span role="presentation">    text: `UID:${guestChantId}` + (blocked ? '被屏蔽' : '没有被屏蔽')</span>
 <span role="presentation">  })</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Send plain text message</span>
 <span role="presentation"> * https://core.telegram.org/bots/api#sendmessage</span>
 <span role="presentation"> */</span>
 <span role="presentation">async function sendPlainText (chatId, text) {</span>
 <span role="presentation">  return sendMessage({</span>
 <span role="presentation">    chat_id: chatId,</span>
 <span role="presentation">    text</span>
 <span role="presentation">  })</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Set webhook to this worker's url</span>
 <span role="presentation"> * https://core.telegram.org/bots/api#setwebhook</span>
 <span role="presentation"> */</span>
 <span role="presentation">async function registerWebhook (event, requestUrl, suffix, secret) {</span>
 <span role="presentation">  // https://core.telegram.org/bots/api#setwebhook</span>
 <span role="presentation">  const webhookUrl = `${requestUrl.protocol}//${requestUrl.hostname}${suffix}`</span>
 <span role="presentation">  const r = await (await fetch(apiUrl('setWebhook', { url: webhookUrl, secret_token: secret }))).json()</span>
 <span role="presentation">  return new Response('ok' in r && r.ok ? 'Ok' : JSON.stringify(r, null, 2))</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">/**</span>
 <span role="presentation"> * Remove webhook</span>
 <span role="presentation"> * https://core.telegram.org/bots/api#setwebhook</span>
 <span role="presentation"> */</span>
 <span role="presentation">async function unRegisterWebhook (event) {</span>
 <span role="presentation">  const r = await (await fetch(apiUrl('setWebhook', { url: '' }))).json()</span>
 <span role="presentation">  return new Response('ok' in r && r.ok ? 'Ok' : JSON.stringify(r, null, 2))</span>
 <span role="presentation">}</span>
 <span role="presentation">​</span>
 <span role="presentation">async function isFraud(id){</span>
 <span role="presentation">  id = id.toString()</span>
 <span role="presentation">  let db = await fetch(fraudDb).then(r => r.text())</span>
 <span role="presentation">  let arr = db.split('\n').filter(v => v)</span>
 <span role="presentation">  console.log(JSON.stringify(arr))</span>
 <span role="presentation">  let flag = arr.filter(v => v === id).length !== 0</span>
 <span role="presentation">  console.log(flag)</span>
 <span role="presentation">  return flag</span>
 <span role="presentation">}</span>
```

修改后保存并部署即可。
然后访问 `https://demo.demo.workers.dev/UUID` 注册 WebSoket 即可。
私聊机器人，各项功能运行正常即可。
