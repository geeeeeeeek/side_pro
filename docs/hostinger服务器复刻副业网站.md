本文介绍在线播放器网站的详细部署过程。

### 准备服务器

- hostinger官网购买
- shell登录

### 部署过程

- 环境配置
- 源码上传
- nginx配置

```
## nginx配置参考
server {
    listen 80;
    server_name example.com www.example.com; # 换成你的域名或服务器IP

    root /var/www/my-website; # 网站文件存放的根目录
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 域名映射

在域名注册地，将域名的dns的A记录解析到服务器ip

### AdSense联盟集成

注册AdSense后，提交网站，集成代码。


