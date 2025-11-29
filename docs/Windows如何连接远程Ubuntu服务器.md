# Windows如何连接远程Ubuntu服务器

### 两种方式

- root+密码方式
- SSH密钥方式

### 常用连接工具

- Xshell
- SecureCRT
- Putty
- Termius
- iTerm2

### 密钥登录步骤

#### 1. 安装puTTY
#### 2. 使用puTTYgen生成密钥，将私钥和公钥保存本地。
#### 3. 复制公钥到远程

```
// 编辑authorized_keys
// vim ~/.ssh/authorized_keys
```

#### 4. 打开密钥登录开关

```
// 打开ssh配置文件
vim /etc/ssh/sshd_config
// 将开关设置为yes 
PubkeyAuthentication yes
// 重启服务
sudo systemctl restart ssh
```

#### 5. secureCRT配置密钥并点击登录

