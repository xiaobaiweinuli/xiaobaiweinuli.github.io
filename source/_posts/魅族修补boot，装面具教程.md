---
title: '魅族修补boot，装面具教程'
date: '2023-12-24 12:28:31'
tags: ['魅族', '面具', '修补boot', '刷机']
description: ''
---

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/volantgoat.png)

最后更新时间：2022年02月09日


# 前言

魅族手机twrp缺少开发者，现存的twrp经常出现无法解密data分区的情况，导致无法读取手机内部存储，解密data需要先格式化data，就意味着要清除手机数据；

装面具除了直接刷卡刷包以外还有一种方式，就是在fastboot模式下刷入修补过的boot镜像，此篇幅教程将会详细为你介绍如何提取、修补、刷入boot镜像；

# 一、准备材料

1. 已经有装有面具的手机一部，可以是自己的也可以不是自己的；

2. 升级目标系统的卡刷包一个，魅族的系统都是update.zip，大小2G左右；

3. 电脑一台；

4. 脑子一个，手一双；

# 二、提取boot

## 1、18系列以下的机型

### 1.1、用手机操作

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot1.svg)

### 1.2、用电脑操作

直接打开压缩包，解压对应的文件即可。

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot2.png)
## 2 、18及18pro机型

### 2.1、先解压出payload.bin
![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot3.png)
### 2.2 使用工具解压payload

工具下载：[点我下载](https://magiskcn.com/payload-dumper-go-boot)

2.2.1 、解压工具，复制 payload.bin 文件到 payload-dumper-go 文件夹里面
![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot4.jpg)
2.2.2 打开CMD命令行
![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot5.jpg)
2.2.3 按照提示输入 b
![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot6.jpg)
2.2.4 提取成功，打开 img 文件夹 就可以看到提取的 boot.img 了
![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot7.jpg)
# 三、修补boot
使用已经装有magisk的手机进行操作，操作流程如下：

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot8.svg)

# 四、刷入boot

## 4.1、电脑操作

### 4.1.1、下载adb工具包

[点击下载](https://team.volantgoat.com/download/60b4bc5412a59a00461a8c75)

### 4.2.2、使用adb工具刷入

解压adb工具包

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot9.png)
将修补好的boot镜像拖到adb文件夹内

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot10.png)
双击 "打开CMD命令行.bat"

![](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%AD%85%E6%97%8F%E4%BF%AE%E8%A1%A5boot11.png)
```Plain Text
#输入如下：
fastboot flash boot  修补boot的镜像名字.img
# 如果是18系列机型，输入如下,一次一行，回车确认：
fastboot flash boot_a  修补boot的镜像名字.img
fastboot flash boot_b  修补boot的镜像名字.img
```

# 五、安装magisk

刷完boot以后，直接开机，安装magisk的软件即可，注意事项：

 -  **安装的版本尽量与修补boot使用的那个magisk版本一致；**


借鉴：
- [魅族修补boot，装面具教程](https://www.volantgoat.com/archives/244/)
- [安装 | KernelSU](https://kernelsu.org/zh_CN/guide/installation.html)
- [payload提取boot.img - Magisk中文网](https://magiskcn.com/payload-dumper-go-boot)