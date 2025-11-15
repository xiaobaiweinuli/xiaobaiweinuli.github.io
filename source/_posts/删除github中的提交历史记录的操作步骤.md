---
title: '删除github中的提交历史记录的操作步骤'
date: '2024-04-19 21:33:10'
tags: ['github']
categories: ['默认分类']
description: ''
toc: 'True'
---
# 安装Git
在Windows上使用Git，可以从Git官网直接[下载安装程序](https://git-scm.com/downloads)，然后按默认选项安装即可。
# 配置Git
## 1.查看当前User和Email配置
```bash
git config --local --list 
git config --list 
```
## 2.设置用户名和邮箱
```bash
git config --global user.name "username"
git config --global user.email  useremail@qq.com
```
## 3.检查是否配置成功
```bash
完成前两步后，可以用下面的命令检查是否配置成功：
git config --global  --list 
```
## 4.生成 SSH 密钥
输入
```bash
ssh-keygen -t ed25519 -C "邮箱"
```
显示
```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/c/Users/YOU/.ssh/id_ed25519):
Created directory '/c/Users/YOU/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```
**输入生成密钥路径，可以接受默认的文件位置，也可以指定一个不同的位置。您在指定路径时提供的应该是一个文件名，而不是一个目录名。例如 “C:\Users\YOU\1234”。这样，ssh-keygen 将会在指定的目录中创建一个名为“1234” 的文件来保存您的私钥，并创建一个名为 “1234.pub” 的文件来保存您的公钥。
然后输入一个密码（passphrase），这是可选的，但建议为了安全性添加一个密码。**

### 修改文档后缀为 .sh 并保存，双击执行脚本自动完成上述操作
```bash
#!/bin/bash
userName="这里改成你的用户名"
email="这里改成你的Email"
# 配置 git 用户名和邮箱
git config --global  user.name ${userName}
git config --global user.email ${email}
git config --global  --list 
echo "Enter 或者 y 键确认"
ssh-keygen -t rsa -C "${email}"
# 打印公钥
echo "复制保存下面的公钥添加到远程仓库"
echo ${splitLine}
cat ~/.ssh/id_rsa.pub
echo ${splitLine}
echo "按任意键退出"
read -n 1
echo "继续运行"
```
## 5.将SSH私钥添加到 ssh-agent
在后台启动 ssh-agent：
```bash
eval $(ssh-agent -s)
```
将SSH私钥添加到 ssh-agent：
```bash
ssh-add c:/Users/YOU/.ssh/id_ed25519
```
## 6.上传 SSH 公钥
复制SSH公钥:
```bash
clip < /c/Users/chenjs/.ssh/id_rsa.pub
```
**Gitee：**点击导航栏右上角头像，选择「设置」，然后在侧边栏菜单选择「SSH 公钥」，填入上一步保存的公钥内容并保存确认。
**GitHub：**点击导航栏右上角头像，选择「Settings」，然后在侧边栏菜单选择「SSH and GPG keys」，填入上一步保存的公钥内容并保存确认。
## 7.测试连接
```bash
ssh -T git@github.com
```
**输入后显示：**
```
The authenticity of host 'github.com (ip)' can't be established.
ED25519 key fingerprint is SHA256:****.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```
**输入yes后显示：**
```
Warning: Permanently added 'github.com' (ED25519) to the list of known hosts.
Hi 用户名! You've successfully authenticated, but GitHub does not provide shell access.
```
如果提示中的用户名是你的，说明SSH key已经配置成功。


# 删除提交历史记录
```bash
##  `初始化一个新的 Git 仓库`
git init
## `添加远程仓库`
git remote add origin git@github.com:用户/仓库名
## `切换到您的本地仓库目录`
cd 仓库名
## `切换到一个脱离主分支的另外一条全新主分支
git checkout --orphan latest_branch
## `暂存所有改动过的文件，内容为当前旧分支的最新版本所有文件`
git add -A
## `提交更改`
git commit -am "commit message"
## `删除原始主分支`
git branch -D main
## `将当前分支重命名为 main`
git branch -m main
## `最后，强制更新您的存储库`
git push -f origin main
```
`处理一次后下回直接执行`
```bash
git remote add origin git@github.com:用户/仓库名 &&
cd 仓库名 &&
git checkout --orphan latest_branch &&
git add -A &&
git commit -am "commit message" &&
git branch -D main &&
git branch -m main &&
git push -f origin main
```
---
# 其它
检查本地主机是否已经存在ssh key：
```
ls -al ~/.ssh
```
---
**问题解决方案**
在配置完成后，通过ssh连接github时，报错：Permission denied (publickey).
大概率是因为：自定义了密钥名字/路径，但没有执行第二个步骤将密钥添加到SSH认证代理中。
可以输入以下命令验证是否生成了密钥以及是否有添加到SSH认证代理中，如果没有就按第二步骤操作一遍。
```
ssh-add -l -E sha256
```
如果配置失败，则没有任何输出；如果配置成功，则会输出类似以下内容：2048 SHA256:274ffWxgaxq/tSINAykStUL7XWyRNcRTlcST1Ei7gBQ /Users/USERNAME/.ssh/id_rsa (RSA)
除了通过ssh-add的方式外，也可以通过设置config文件让SSH认证代理能找到这个密钥文件，从而解决这个问题：
```
# 打开（如果没有就创建一个）config文件，并输入以下内容。
# 此外，需要注意，config文件的权限需是600。
Host github.com
    HostName github.com
    IdentityFile ~/.ssh/github_auth # 这里输入你的密钥路径
```
在配置好SSH后，进行git操作时，仍要求输密码，即使输入了正确的账户和密码，还是报错：
```
remote: Support for password authentication was removed on August 13, 2021. Please use a personal access token instead.
remote: Please see https://github.blog/2020-12-15-token-authentication-requirements-for-git-operations/ for more information.
fatal: Authentication failed for 'https://github.com/xxx/xxx.git/'
```
出错的原因在于：本地仓库在clone时使用的是HTTPS URL，故该仓库此时的remote协议会是HTTPS协议，然而SSH密钥连接只支持SSH URL，不支持HTTPS URL，故会要求输账户密码。
此时，通过以下命令可以查看到仓库的remote协议是HTTPS协议：
```
git config --get remote.origin.url
```
如果输出类似以下内容，则说明remote协议是HTTPS协议
```
https://github.com/xxx/xxx.git
```
也可以查看仓库内的.git/config文件，查看url是git协议还是https协议。
```
 [remote "origin"]
   url = https://github.com:YOUR_ACCOUNT/YOUR_PROJECT.git
   fetch = +refs/heads/*:refs/remotes/origin/*
```
因此，需要将remote协议从HTTPS协议修改为GIT协议。在本地仓库路径下输入以下命令：
```
git remote set-url origin git@github.com:xxx/xxx.git
```
此时，再进行git的pull/push操作就不再需要输密码了，直接可以通过SSH密钥认证。

---

**添加或更改密码**
```
$ ssh-keygen -p
Enter file in which the key is (/c/Users/asua/.ssh/id_rsa): # 如果你的密钥就在默认位置，直接回车就行，如果不是，就手动输入
Key has comment 'hahaha@gmail.com' # 之前生成密钥时，我输入的内容
Enter new passphrase (empty for no passphrase): # 输入新密码
Enter same passphrase again: # 再次输入密码
Your identification has been saved with the new passphrase. # 身份信息和密码一起保存
```
**ssh-agent在Git for Windows上自启动**
你可以在打开 bash 或 Git shell 时自动运行 ssh-agent。 复制以下行并将其粘贴到 Git shell 中的 ~/.profile 或 ~/.bashrc 文件中：
```
env=~/.ssh/agent.env

agent_load_env () { test -f "$env" && . "$env" >| /dev/null ; }

agent_start () {
    (umask 077; ssh-agent >| "$env")
    . "$env" >| /dev/null ; }

agent_load_env

# agent_run_state: 0=agent running w/ key; 1=agent w/o key; 2= agent not running
agent_run_state=$(ssh-add -l >| /dev/null 2>&1; echo $?)

if [ ! "$SSH_AUTH_SOCK" ] || [ $agent_run_state = 2 ]; then
    agent_start
    ssh-add
elif [ "$SSH_AUTH_SOCK" ] && [ $agent_run_state = 1 ]; then
    ssh-add
fi

unset env
```
如果你的私钥没有存储在默认位置之一（如 `~/.ssh/id_rsa`），你需要告知 SSH 身份验证代理其所在位置。 要将密钥添加到 `ssh-agent`，请输入 `ssh-add ~/path/to/my_key`。
如果想要` ssh-agent` 在一段时间后忘记您的密钥，可通过运行` ssh-add -t <seconds> `进行配置。
现在，当您初次运行 Git Bash 时，系统将提示您输入密码：
```
> Initializing new SSH agent...
> succeeded
> Enter passphrase for /c/Users/you/.ssh/id_rsa:
> Identity added: /c/Users/you/.ssh/id_rsa (/c/Users/you/.ssh/id_rsa)
> Welcome to Git (version 1.6.0.2-preview20080923)
>
> Run 'git help git' to display the help index.
> Run 'git help ' to display help for specific commands.
```
ssh-agent 进程将继续运行，直到您注销、关闭计算机或终止该进程。
如果没有 ~/.profile 或 ~/.bashrc 文件，则自己创建一个：
```
$ touch ~/.profile # 在/c/Users/username路径下新建.profile文件，就是和.ssh文件在同一个目录下
```
用文本编辑器（Notepad++或者vim）打开.profile文件，将上面的脚本代码复制到.profile文件中保存后退出，重新打开Git Bash后，输入SSH的密码即可。

---
**一台机器上管理多个GitHub账号的SSH密钥**
如果你在一台机器使用两个github账号（比如私人账号abc和工作账号xyz），两个帐号用不同的SSH KEY，还需要编辑一下配置文件~/.ssh/config：
```
Host personal.github.com  
    HostName github.com  
    User git  
    IdentityFile ~/.ssh/personal_rsa  
    
Host work.github.com  
    HostName github.com  
    User git  
    IdentityFile ~/.ssh/work_rsa
```
- Host： "personal.github.com"是一个"别名"，可以随意命名。
- HostName：比如我工作的git仓储地址是git@code.sleep.com:username/repo_name.git, 那么我的HostName就要填"sleep.com"；
- IdentityFile： 所使用的公钥文件;
配置完毕，用下面的命令测试一下：
```
ssh -T git@personal.github.com
ssh -T git@work.github.com
# 注： @符号后面的"personal.github.com"就是在~/.ssh/config文件中指定的"Host"项
```
1.为已经检出的repository指定github账号：
在已经检出的repos目录下执行:
```
git config  user.name "your-id"
git config  user.email "your-id@gmail.com"
```
修改.git/config并找到[remote "origin"],修改url的值为：
```
[remote "origin"]   
    url = git@personal.github.com:user_name/repos_name.git
```
其中, personal.github.com就是在配置文件~/.ssh/config中的Host项, 设置完成后, 在这个工程目录git push会自动以此git帐号提交代码。
2.使用指定账号clone已存在的repository：
- 使用指定账号clone一个已经存在的repos:
git clone git@personal.github.com:user_name/repos_name.git, 上面命令中的"personal.github.com"就是在～/.ssh/config文件中指定的"Host"项, "user_name"是指定提交代码的账户名。
- 然后还需要git config一下user.name和user.email, 进入repository目录执行:
```
git config user.name your_name
git config user.email your_email
```
以后在此repos下git push origin master就是使用指定的用户push.
3.使用指定账号git init新的repository：
```
$ git init
$ git add .
$ git commit -m "first commit"
$ git remote add origin git@personal.github.com:user_name/testing.git
$ git push -u origin master
```
---
### 参考转存：
#### GitHub官方教程：[通过 SSH 连接到 GitHub](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)
#### [Github配置SSH密钥连接（附相关问题解决）](https://zhuanlan.zhihu.com/p/628727065)
#### [使用SSH连接到GitHub - 简书](https://www.jianshu.com/p/9a36ba848d4d)