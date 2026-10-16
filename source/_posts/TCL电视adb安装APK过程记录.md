---
title: TCL 电视 adb 安装第三方 APK 记录
tags:
  - adb
  - TCL
categories:
  - 教程
description: 记录在 TCL 定制 Android 11 电视上通过 adb 侧载第三方 APK 的踩坑与解决过程，四个系统开关全部无效后，最终靠禁用系统安装器完成安装。
date: 2026-10-11 16:14:56
footer:
  references:
    - '[https://github.com/wukongdaily/tvhelper-docker/issues/8#issuecomment-3894652199](https://github.com/wukongdaily/tvhelper-docker/issues/8#issuecomment-3894652199)'
    - '[https://tieba.baidu.com/p/9833857070#](https://tieba.baidu.com/p/9833857070#)'
---

> 进入设置 > 系统 > 系统信息，遥控器依次按下"上"、"下"、"左"、"右"，即可看到页面中跳出 adb 开关，将 ADB 设为开启状态。

# TCL 电视 APK 侧载记录

**设备**：192.168.31.26:5555 — TCL 定制 Android 11（SDK 30），纯 32 位 armeabi-v7a，无 root/su
**目标**：把本机 `/storage/emulated/0/Download/leanback-armeabi_v7a.apk` 推到设备并安装
**结果**：✅ 安装成功（`com.fongmi.android.tv`）

---

## 一、失败路径汇总

> `pm install /sdcard/...` 会先被 SELinux 挡掉（system_server 读不了 `u:object_r:fuse:s0`）。

### 1. 四个开关全部无效 ❌

`INSTALL_FAILED_VERIFICATION_FAILURE`，依次尝试：

| 开关 | 设定值 | 结果 |
| --- | --- | --- |
| `persist.tcl.debug.installapk` | `1` | ❌ 无效 |
| `persist.tcl.installapk.enable` | `1` | ❌ 无效 |
| `package_verifier_enable` | `0` | ❌ 无效 |
| `verifier_verify_adb_installs` | `0` | ❌ 无效 |

**设置确认写入成功**（复查已生效），但安装照旧被拒。

**根因诊断**：

```text
[settings 层面]  package_verifier_enable = 0  ✓ 已关
[真正拦截者]     Verifiers:
                   Required: com.android.packageinstaller (uid=10012)
                 ro.feature.packageinstaller_risk_detection = true   ← 只读 prop
```

TCL 在 `com.android.packageinstaller` 里加了**自己的安装风险检测**（`ro.feature.packageinstaller_risk_detection=true`，运行时不可改），校验走这个组件，**不读那两个 settings**。两个 `persist.tcl.*` prop 需重启才被读取，且非根因。

→ **结论：靠这四个开关在这台设备上完全绕不过安装限制。**

---

### 2. 转向禁用系统安装器 ⚠️

```sh
adb shell pm disable-user --user 0 com.android.packageinstaller
# → Package com.android.packageinstaller new state: disabled-user  ✓ 禁用成功

adb install xxx.apk
```

> ⚠️ 注意：为了避免影响系统正常使用，安装完成后记得恢复。

```sh
adb shell pm enable com.android.packageinstaller
```

---

## 二、恢复清单

```text
                    改动时  →  恢复后
verifier_verify_adb_installs    0    →     1  ✓
package_verifier_enable         0    →     1  ✓
persist.tcl.debug.installapk    1    →     0  ✓
persist.tcl.installapk.enable   1    →     0  ✓
com.android.packageinstaller    disabled-user  →  enabled  ✓
```

最终复核：

```text
[enabled 列表]   package:com.android.packageinstaller
[disabled 列表]  空
[详细状态]       User 0: enabled=1  installed=true  hidden=false  stopped=false
```

> ⚠️ **禁用安装器后忘记恢复，会导致系统更新卡死 → 只能恢复出厂设置。**

