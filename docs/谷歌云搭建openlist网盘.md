> 本文分享使用谷歌云免费服务器搭建openlist网盘聚合网站。

### 准备条件

- 服务器
- 域名

### 搭建步骤

- 使用openlist的一键安装脚本安装
- 后台配置，集成驱动

### 绑定域名

- 配置nginx
- 域名dns解析


### 集成AdSense联盟

- 准备广告代码
- 点击后台全局，设置自定义头部



### nginx参考配置

```
server {
  listen 80;
  server_name pan.yourdomain.com; # 换成你的域名
  location / {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Range $http_range;
    proxy_set_header If-Range $http_if_range;
    proxy_redirect off;
    # 下面这一行的端口要改为你一键脚本运行的真实端口
    proxy_pass http://127.0.0.1:3000; 
    # 上传大小限制，防止大文件上传失败
    client_max_body_size 0;
  }
}
```


### 参考资料

openlist官网文档

https://doc.oplist.org/

token获取方式

https://api.oplist.org/
