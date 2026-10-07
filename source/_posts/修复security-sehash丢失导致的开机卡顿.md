---
title: 修复 security.sehash 丢失导致的开机全盘扫描卡顿
date: 2026-10-07 12:21:11
categories:
  - Android
tags:
  - MIUI
  - SELinux
  - KernelSU
description: 记录一下解决 Android 开机在第一屏卡顿 1~2 分钟的过程。针对 security.sehash 无法持久化保存导致每次开机触发全盘 restorecon 的问题，利用 Linux Unshare 隔离挂载点快速生成并写回 sehash 的操作。
---
> 解决某些系统（如 MIUI/HyperOS）由于 init 阶段 restorecon 逻辑异常导致的开机卡第一屏 1~2 分钟的问题。

## 问题背景与原理
在 Android 系统开机的 `post-fs-data` 早期阶段，`init` 进程会对 `/data` 目录执行一次 `restorecon` 操作，确保其下所有文件和目录都拥有正确的 `SELinux Label`。
 * 正常的机制：系统只会在更新或 `SELinux` 策略变更时完整扫描 `/data`。扫描成功后，`init` 会将基于 `/system/etc/selinux/plat_file_contexts` 计算出的 Hash（精简后的 Sha256 签名）存储在 /data 节点的扩展属性 security.sehash 中。下次开机时，比对 Hash 一致就会直接跳过扫描。
 * BUG 根源：某些设计不良的系统（尤其是 `MIUI`），因为策略规则配置不当或个别文件节点报错，导致 `restorecon` 无法顺利走完，永远无法把 Hash 写回 `security.sehash`。
 * 表现与后果：系统每一次开机都会退化为 O(N) 复杂度的全局扫描。系统中的文件越多（如微信聊天记录、图片、程序数据等），开机第一屏卡顿的时间就越长（通常 1~2 分钟以上）。此时系统未加载 adbd，也未进入第二屏开机动画，极易被误判为“卡砖”。
## 解决思路：O(1) 伪装避坑法
既然全盘扫描极慢且容易出错，我们可以利用 Linux 的 Mount Namespace (隔离挂载点) 制造一个假的空 /data：
 * 在私有隔离环境中将一个空目录 --bind 到 /data。
 * 对空的 /data 执行 restorecon——因为没有复杂文件，只需 0.01 秒即可瞬间成功并生成当前系统有效的 security.sehash。
 * 读取导出的有效 Hash 数据。
 * 恢复真正的 /data 目录，并将这串 Hash 强制写入真实 /data 节点的扩展属性中。
> 提示：不需要使用 tmpfs 内存文件系统，因为 restorecon 会跳过伪文件系统；使用 unshare -m 进行 Mount Namespace 隔离可以保障系统其他运行进程不受任何干扰。

```
#获取root权限
su
# 在私有隔离 ns 中操作
/data/adb/ksu/bin/busybox unshare -m sh
# 制造一个假的空 /data 目录
mkdir /data/tmp
mount --bind /data/tmp /data
# 因为 /data 没有文件，restorecon 只会修改目录自身的 label 并记录 hash
restorecon -Rv /data
# 从假 /data 获取当前系统下 /data 的 sehash：getfattr -n security.sehash /data
toybox getfattr --only-values -n security.sehash /data > /dev/sehash.bin
# 把真正的 /data 目录的 sehash 修改为上面得到的 hash
umount /data
toybox setfattr -n security.sehash -v "$(cat /dev/sehash.bin)" /data
```

## 排坑与补充说明
 * Magisk 用户的额外注意事项：如果需要执行全盘 restorecon -Rv /data，请务必先给 /data/adb/modules 盖一层 tmpfs 隔离，否则 Magisk 模块的文件 Context 可能会被意外重置引发挂载故障。
 * 系统更新/刷机后处理：由于 `security.sehash` 是与 `/system/etc/selinux/plat_file_contexts`（即当前的系统镜像版本）强绑定的，当后续对手机系统进行 OTA 大版本升级或更新 ROM 后，系统 Hash 将改变。如果更新后再次出现第一屏卡顿，重新逐步运行上面代码或者运行下面的文件即可。
 * 如仍未解决：若手动补全 `security.sehash` 后第一屏耗时依然极长，说明开机瓶颈不在于 `restorecon`。建议在开机后获取开机日志分析根因：dmesg > /sdcard/dmesg_boot.txt

参考：https://t.me/real5ec1cff/79
感谢：TG @DeeppSeeek
文件另存：https://t.me/xingshuang_blog/208