---
title: '使用DSU Sideloder实现安卓双系统|'
date: '2024-05-08 12:14:01'
tags: []
categories: ['默认分类']
description: ''
toc: 'True'
---
准备
首先需要确保手机自带DSU Loader功能:

只需打开开发者模式, 往下翻动即可看到DSU Loader的字样(不用翻很多), 如果没有的话, 说明设备不支持.

只要看到这个选项就行, 不需要点它.

这个功能大概率在出厂即为安卓12的手机上有.

随后, 去谷歌商店下载一个检测软件:

[https://play.google.com/store/apps/details?id=tk.hack5.treblecheck](https://play.google.com/store/apps/details?id=tk.hack5.treblecheck)

安装好后, 若显示如下字样, 则说明可以继续:

![如图所示](https://img-blog.csdnimg.cn/direct/dfa8ecb425334c2e861c759a63b06fc9.png)

点击浏览映像, 选择其中的一个系统并下载其镜像.

我目前使用的是Unofficial Android 13中的Evolution X, 除了不能收短信以外, 其他都正常.

我也很奇怪, 只能发不能收…

当然了, 反正是双系统, 你可以多试几个.

那么, 问题来了, 怎么试呢?

开始
首先下载DSU Sideloader: [https://github.com/VegaBobo/DSU-Sideloader/releases/download/2.03/app-release.apk](https://github.com/VegaBobo/DSU-Sideloader/releases/download/2.03/app-release.apk) 并安装.

不过在开始安装之前, 容我以简单的语言表述我对这一双系统原理的浅显理解:

这是官方的说法: [https://developer.android.com/topic/dsu?hl=zh-cn](https://developer.android.com/topic/dsu?hl=zh-cn)

实际上, 这功能就是给安卓开了一个新分区, 使得类似于电脑上的一个主板系统可以检测到此系统, 并让其启动.

还记不记得上节说的KernelSU, 就是在开机的时候的boot分区上”做了手脚”, 从而获取了root权限.

那么, 为何不能也做做手脚, 在手机开机的时候多一个启动项呢?

我个人认为, 这过程就跟BIOS的作用一样, 大同小异.

好了, 不再扯皮! 扯点别的.

为什么我们不用在设置里看到的DSU Loader呢?

设置里的这个Loader, 默认只提供了谷歌原生的镜像, 而正是因为我们要体验类原生, 所以不用系统自带的这个入口, 继而使用Sideloader这个第三方软件添加双系统.

如果你想体验谷歌的原生安卓, 可以不使用DSU Sideloader.

OK!

下载好了镜像, 我们打开DSU Sideloader.

DSU Sideloader不需要root权限即可运行, 只需要电脑adb授予权限即可, 不过我没有试过adb那种, 因为我的手机已经root啦!



点击选择一个要安装的GSI文件并选择我们刚刚下载好的镜像, 下面的DSU用户空间大小即为要分给此系统的储存大小, 我的手机是1T, 所以非常豪迈地分了128给它!

设置好一切后, 点击安装, 耐心等待即可.

待安装好双系统后, DSU Sideloader出现以下字样:

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/4974ad91263148e4b57fa0df4df4e2ee.png)


同时通知栏会出现一个常驻的清理不掉的通知:
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/4cac6270c1474469b3a11458c21ef16b.png)



切记莫点舍弃! 否则花那么久安装的双系统直接扼杀在摇篮里了.

怎么启动到双系统呢?

只需打开DSU Sideloader, 或从那个常驻通知中点击重启即可.

永久双系统
如果上面的步骤都跟着来的话, 现在的你应该已经在使用另一个系统了(简称b系统).

此时, 若要回到原系统, 只需在双系统中重启即可.

那有没有什么办法, 让我在b系统中重启, 还不回到原系统呢?

答案是肯定的.

有两种方法, 如果你有电脑, 只需在adb连上b系统后, 输入:

1
adb shell gsi_tool enable
即可.

如果是Linux系统, 且手机被root, 会提示permission不够, 加sudo就行.

如果没有电脑, 需要在b系统中安装Termux与KernelSU, 同时让KernelSU给Termux授予root权限.

打开Termux, 输入su回车, 再输入:

1
gsi_tool enable
出现如下字样则说明成功:


![在这里插入图片描述](https://cdn.jsdelivr.us/gh/xiaobaiweinuli/bloglmage@main/img/%E9%87%8D%E5%90%AF%E6%8D%A2%E7%B3%BB%E7%BB%9F)

此时b系统进入重启后还是b系统模式, 若要退出此模式, 只需将上述指令中的enable换成disable, 再次执行即可.
