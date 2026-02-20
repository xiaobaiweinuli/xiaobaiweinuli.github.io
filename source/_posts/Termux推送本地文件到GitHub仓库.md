---
title: 'Termux推送本地文件到GitHub仓库'
date: '2024-04-21 18:51:45'
tags: ['Termux', 'Github', 'ssh']
description: ''
---
如果您已在电脑上配置好了SSH密钥，并将相关文件（`id_ed25519`、`id_ed25519.pub`、`known_hosts`）移动到了手机的目录下，接下来您需要在手机上的Git环境中正确配置SSH，以便使用这些密钥与GitHub进行通信。以下是针对Android设备使用Termux进行SSH配置的步骤：
### **前提条件**
确保您已经安装了Termux应用，并在其中安装了Git。如果您尚未安装，请按照以下步骤操作：
1. **安装Termux**：访问Google Play Store或第三方应用市场，搜索并安装Termux应用。
2. **在Termux中安装Git**：
   ```bash
   pkg update
   pkg install git openss
   ```
### **配置SSH密钥和known_hosts**
**步骤1：创建SSH目录**
在Termux中，创建一个与您的用户关联的`.ssh`目录（如果尚未存在）：
```bash
mkdir -p ~/.ssh
```
**步骤2：移动密钥文件**
将之前移动到手机的密钥文件复制到刚创建的`.ssh`目录下：
```bash
mv /目录/id_ed25519* ~/.ssh/
mv /目录/known_hosts ~/.ssh/
```
**步骤3：设置权限**
确保SSH密钥文件只有您自己能读写：
```bash
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 644 ~/.ssh/known_hosts
```
### **测试SSH连接**
现在，您可以尝试使用SSH连接到GitHub以验证配置是否正确：

```bash
ssh -T git@github.com
```
系统可能会提示您确认主机指纹，如果指纹与您之前在电脑上添加的GitHub服务器指纹一致，则回答`yes`。如果一切正常，您应该看到类似于“Hi [username]! You've successfully authenticated, but GitHub does not provide shell access.”的消息。
### **使用SSH密钥克隆或操作Git仓库**
配置好SSH后，您就可以使用SSH URL克隆、拉取或推送Git仓库了。例如，要克隆一个私有仓库：
```bash
git clone git@github.com:username/repo.git
```
这里的`username`和`repo`分别替换为您自己的GitHub用户名和仓库名。

至此，您已经在手机的Termux环境中成功配置了从电脑迁移过来的SSH密钥，并能够使用它们进行Git操作。如果您计划在多个项目中使用这些密钥，无需重复以上步骤，因为它们已经在全局的`~/.ssh`目录下被设置为默认的SSH身份验证方式。
### **Python推送本地文件到Githb**
```python
import os
import subprocess
import tempfile
import shutil
# 配置您的GitHub用户名、仓库名、本地文件路径以及目标分支
GITHUB_USER = "GitHub用户名"
REPO_NAME = "仓库名"
LOCAL_FILE_PATH = "本地文件路径"
TARGET_BRANCH = "目标分支"
# 设置Git相关配置
os.environ["GIT_AUTHOR_EMAIL"] = "邮箱"
os.environ["GIT_AUTHOR_NAME"] = "GitHub用户名"
# 初始化临时目录并克隆仓库（使用SSH方式）
with tempfile.TemporaryDirectory() as TEMP_DIR:
    os.chdir(TEMP_DIR)
    subprocess.run(["git", "clone", "--depth=1", f"git@github.com:{GITHUB_USER}/{REPO_NAME}.git"])
    # 将本地文件复制到临时目录的仓库中
    shutil.copy(LOCAL_FILE_PATH, os.path.join(TEMP_DIR, REPO_NAME))
    # 进入仓库目录
    os.chdir(os.path.join(TEMP_DIR, REPO_NAME))
    # 添加文件、提交更改并推送至目标分支
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Update video.txt from local"])
    subprocess.run(["git", "push", "origin", TARGET_BRANCH])
print("File successfully pushed to GitHub repository.")
```
### **Shell推送本地文件到Githb**
```bash
 #!/bin/bash
# 配置您的GitHub用户名、仓库名、本地文件路径以及目标分支
GITHUB_USER="GitHub用户名"
REPO_NAME="仓库名"
LOCAL_FILE_PATH="本地文件路径"
TARGET_BRANCH="目标分支"
# 设置Git相关配置
git config --global user.email "邮箱"
git config --global user.name "GitHub用户名"
# 初始化临时目录并克隆仓库（使用SSH方式）
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"
git clone --depth=1 "git@github.com:$GITHUB_USER/$REPO_NAME.git"
# 将本地文件复制到临时目录的仓库中
cp "$LOCAL_FILE_PATH" "$TEMP_DIR/$REPO_NAME/"
# 进入仓库目录
cd "$TEMP_DIR/$REPO_NAME"
# 添加文件、提交更改并推送至目标分支
git add .
git commit -m "Update video.txt from local"
git push origin "$TARGET_BRANCH"
# 清理临时目录
cd ..
rm -rf "$TEMP_DIR"
echo "File successfully pushed to GitHub repository."
```