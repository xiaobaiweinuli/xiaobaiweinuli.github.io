---
title: '红米K60刷入KSU'
date: '2023-12-27 13:19:07'
tags: ['红米K60', 'KSU', '刷机']
categories: ['默认分类']
description: ''
toc: 'True'
---

## 准备

1.获取你手机的原厂 boot.img；你可以通过你手机的线刷包解压后之间获取，如果你是卡刷包，那你也许需要[payload-dumper-go](https://magiskcn.com/payload-dumper-go-boot)
> **参考：**[魅族修补boot，装面具教程](https://xiaobaiweinuli.github.io/post/pq9yCdjaw/)

2.下载 KernelSU 提供的与你设备 KMI 版本一致的 [AnyKernel3](https://github.com/tiann/KernelSU/releases) 刷机包。
3.解压缩 AnyKernel3 刷机包，获取其中的 Image 文件，此文件为 KernelSU 的内核文件。

### 使用 Android-Image-Kitchen修补boot.img

1.下载 [Android-Image-Kitchen](https://forum.xda-developers.com/t/tool-android-image-kitchen-unpack-repack-kernel-ramdisk-win-android-linux-mac.2073775/) 至你电脑。
2.将手机原厂 boot.img 放入 Android-Image-Kitchen 根目录。
3.在 Android-Image-Kitchen 根目录执行unpackimg.bat；此命名会将 boot.img 拆开，你会得到若干文件。（不能执行较大概率为目录问题）
4.将split_img 目录中的 boot.img-kernel 替换为你从 AnyKernel3 解压出来的 Image。`注意名字改为 boot.img-kernel`
5.在 Android-Image-Kitchecn 根目录执行 repackimg.bat；此时你会得到一个 image-new.img 的文件；使用此 boot.img 通过 fastboot 刷入即可。

### 使用magiskboot修补boot.img

1.下载 [magiskboot](https://mrzzoxo.lanzoui.com/b02r7q0dg)：来自[KernelSU中文网](https://kernelsu.com/magiskboot)
2.将手机原厂 boot.img 放入 magiskboot 根目录
3.打开CMD命令行.bat，输入 u 解包boot.img，解包完成，可以看到内核文件：kernel
4.将 AnyKernel3目录 的 Image 重命名为 kernel 并复制到 magiskboot 目录 替换。
5.打开 CMD命令行.bat，输入 r 重新打包


### 将 boot.img 刷入设备

使用 adb 连接您的设备，然后执行 adb reboot bootloader 进入 fastboot 模式，然后使用此命令刷入 KernelSU：
```sh
fastboot flash boot boot.img
```

> 如果你的设备支持 fastboot boot，可以先使用 fastboot boot boot.img 来先尝试使用 boot.img 引导系统，如果出现意外，再重启一次即可开机。

借鉴：
- [安装 | KernelSU](https://kernelsu.org/zh_CN/guide/installation.html)
- [payload提取boot.img - Magisk中文网](https://magiskcn.com/payload-dumper-go-boot)
- [magiskboot（手动修补KernelSU](https://kernelsu.com/magiskboot)