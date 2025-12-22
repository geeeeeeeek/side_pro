##  Ubuntu 上使用 fail2ban 可以有效防止 SSH 暴力破解
 
### 安装 fail2ban

打开终端，运行：
```
sudo apt update
sudo apt install fail2ban
```

### 修改配置

fail2ban 默认的配置文件在 /etc/fail2ban/jail.conf，但不要直接修改此文件。我们推荐新建 /etc/fail2ban/jail.local 以便自定义。

创建和编辑 jail.local
```
sudo vim /etc/fail2ban/jail.local
```

添加你需要的配置。例如，针对 SSH 添加如下内容（结合你的需求）：
```
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 6
findtime = 300
bantime = 86400
```
```
参数说明
enabled：启用该 jail
port：监听 SSH 端口（如有自定义端口请替换）
logpath：监控的日志文件（默认 SSH 登录失败都会写入这里）
maxretry：连续失败次数
findtime：在该时间段（秒）内统计 maxretry 次失败
bantime：封禁时间（秒）
```

### 启动并设置自启动

```
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo systemctl restart fail2ban （重启）
```

### 查看运行状态

```
整体服务状态：
sudo systemctl status fail2ban
查看 sshd jail 守护详细信息：
sudo fail2ban-client status sshd
```

### 手动解封某IP（如测试时被误封）

```
sudo fail2ban-client set sshd unbanip <被封IP地址>
```

