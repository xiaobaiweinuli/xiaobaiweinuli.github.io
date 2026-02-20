---
title: '使用Gridea搭建自己的导航站'
date: '2024-04-19 23:34:45'
tags: ['Gridea', '导航']
description: ''
---
### 搭建过程
1. 由于我已在Github Pages下使用Gridea搭建了我的博客[星霜](https://xiaobaiweinuli.github.io/)，因此新建一个Github仓库，启用了pages功能。
2. 将[gridea-theme-webstack](https://github.com/lmm214/gridea-theme-webstack)的文件夹放到配置文件夹的theme文件夹下，重启软件，在设置中切换到该主题并保存，预览应该就可以看到一个空的导航站了。
3. 在主题-自定义配置中添加导航站中的网站信息，包括：名称、地址、图片和描述。在网站添加完成后保存预览，一个导航站就完成了。

### 如何配置分类
该主题默认有四个分类，如果需要添加或者调整分类需要手动更改<a href="#config" style="font-weight: bold; color: red;">config.json</a>和<a href="#index" style="font-weight: bold; color: red;">index.ejs</a>，主题的文件目录如下：
```json
├── assets
│   ├── media
│   │   ├── css
│   │   │   ├── fonts
│   │   │   │   ├── icomoon.eot
│   │   │   │   ├── icomoon.svg
│   │   │   │   ├── icomoon.ttf
│   │   │   │   └── icomoon.woff
│   │   │   ├── icomoon.css
│   │   │   └── main.css
│   │   ├── images
│   │   │   ├── favicon.png
│   │   │   └── logo-collapsed@2x.png
│   │   └── js
│   │       ├── bootstrap.min.js
│   │       ├── jquery-1.11.1.min.js
│   │       ├── lozad.js
│   │       ├── xenon-custom.js
│   │       └── xenon-toggles.js
│   └── styles
│       └── main.less //空文件
├── config.json
└── templates
    ├── archives.ejs //空文件
    ├── index.ejs
    ├── post.ejs //空文件
    ├── tag.ejs //空文件
    └── tags.ejs //空文件
```
1.如果你只是需要更改分类的名称，在<a href="#config" style="font-weight: bold; color: red;">config.json</a>中只需将文件中的`label`和`group`进行更改即可，然后更改<a href="#index" style="font-weight: bold; color: red;">index.ejs</a>。
2.如果你需要添加分类，首先在<a href="#config" style="font-weight: bold; color: red;">config.json</a>中复制添加一个相同的组，并将`name`更改与其他不同，例如更改为`fun6`,`label`和`group`更改为你想要的名称。
<a id="config"></a>
```json
 {
  "name": "fun6",
  "label": "素材资源",
  "group": "素材资源",
  "type": "array",
  "value": [],
  "arrayItems": [
    { "label": "名称", "name": "siteName", "type": "input", "value": "" },
    { "label": "链接", "name": "siteLink", "type": "input", "value": "" },
    { "label": "Logo", "name": "siteLogo", "type": "input", "value": "" },
    { "label": "描述", "name": "description", "type": "input", "value": "" }
  ],
```

3.将如下图的每个类似代码段中的名称更改为与<a href="#config" style="font-weight: bold; color: red;">config.json</a>中对应`name`下的名称：
<a id="index"></a>
```ejs
                    <% if (site.customConfig.fun6) { %>
                    <li>
                        <a href="#素材资源" class="smooth">
                            <i class="icon-inbox"></i>
                            <span class="title">素材资源</span>
                        </a>
                    </li>
                    <% } %>
```
注意代码端中的`site.customConfig.xxxx`要与<a href="#config" style="font-weight: bold; color: red;">config.json</a>中的`name`相对应。
```ejs
        <!-- 素材资源 -->
        <% if (site.customConfig.fun6) { %>
        <h4 class="text-gray"><i class="icon-inbox" style="margin-right: 7px;" id="素材资源"></i>素材资源</h4>
        <div class="row">
            <% site.customConfig.fun6.forEach(function(fun) { %>
            <div class="col-sm-3">
                <div class="xe-widget xe-conversations box2 label-info" onclick="window.open('<%= fun.siteLink %>', '_blank')" data-toggle="tooltip" data-placement="bottom" title="" data-original-title="<%= fun.siteLink %>">
                    <div class="xe-comment-entry">
                        <a class="xe-user-img">
                            <img <% if (fun.siteLogo) { %> data-src="<%= fun.siteLogo %>" <% } else { %> avatar="<%= fun.siteName %>" <% }; %> class="lozad img-circle" width="40">
                        </a>
                        <div class="xe-comment">
                            <a href="#" class="xe-user-name overflowClip_1">
                                <strong><%= fun.siteName %></strong>
                            </a>
                            <p class="overflowClip_2"><%= fun.description %></p>
                        </div>
                    </div>
                </div>
            </div>
            <% }); %>
        </div>
        <br />
        <% } %>
```
注意： 若要添加分类，需要复制添加<a href="#index" style="font-weight: bold; color: red;">index.ejs</a>中的2个代码段，并更改`site.customConfig.xxxx`，以及代码段中的名称，并需要与<a href="#config" style="font-weight: bold; color: red;">config.json</a>中的`name`和`name对应数组的内容相匹配。 