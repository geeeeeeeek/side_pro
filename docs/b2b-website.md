

> 本文介绍如何自己搭建独立站 并且部署到服务器。 [这个网站](https://packdiy.com/)就是我自己完全使用AI搭建的独立站，纯静态html网站，算是我的一个教学案例网站。 里面没有用到wordpress也没有用到后台技术 就是一个纯静态网站。是一个展示型B2B外贸独立站。 自己搭建独立站的优势非常大，因为自己对网站有100%的掌握权，可以随便的修改代码、修改样式、seo优化等等，那假如你使用wordpress或其它平台 修改起来是相当费劲的。 毕竟大多数用独立站的用意就是为了展示自己的产品、产品也没有那么复杂，外贸获客也不是靠独立站，独立站只是展示用的。下面我就使用我的教学案例网站来演示独立站搭建的全过程。 所以如果你不想找人搭建，想自己搭建，可以参考我的教程。very easy



### 大概步骤：

- 第一步：AI编写代码
- 第二步：域名和服务器配置

第一步是编写代码，相关的AI工具太多了，像Codex、Trae、Claude 一大堆。你比如我使用的是Trae 来写代码，直接Ctrl+U就能直接和Agent聊天，一步一步的沟通。达到最终自己满意的页面。告诉Agent 你的网站的背景、你的产品、你的菜单，一般来说 90%的人来说，其实4个菜单就够用了，Home Products About Contact 4个页面。可以边写代码边看结果。我一般是在本地电脑使用python搭建一个简易的环境来运行效果。也很easy，使用 python -m http.server 来运行网站。直到所有的页面都满意了后我才上传到服务器。

![AI代码工具](https://github.com/geeeeeeeek/side_pro/blob/master/docs/raw/b2b-trae.jpg)

第二步就是配置服务器和域名了。 需要自己购买服务器和域名，你比如我服务器是在[hostdare](https://bill.hostdare.com/aff.php?aff=4286)购买的，域名是在hostinger购买的，服务器购买后，只需要安装2个软件就满足网站部署条件，这2个软件是：Nginx和Certbot， 在服务器安装nginx也很easy，直接运行 apt install nginx， 安装Certbot也超简单：sudo apt install certbot python3-certbot-nginx ，如果安装过程遇到问题直接问chatgpt。然后将写的代码上传到服务器，我使用flashfxp工具来上传，然后再使用nginx来配置网站目录，将nginx在本地电脑写到直接上传到远程服务器。然后将自己购买的域名dns解析到服务器ip。整个过程也很easy。另外还有SSL证书配置，使用Certbot来配置就够用了，它提供免费证书而且自动续期。ssl证书申请命令是：

`sudo certbot --nginx -d XXXXX.com -d www.XXXXX.com` 

其中xxxxx.com是你自己的域名。 

nginx重启命令是：`nginx -s reload`





nginx配置说明：

```

server {

  listen 80;

  listen [::]:80;

# 域名配置

  server_name xxxxx.com www.xxxxx.com;

  # 静态 HTML 文件的存放路径

  root /var/www/yourdomain;

  # 默认首页文件名称

  index index.html index.htm;

  location / {

    try_files $uri $uri/ =404;

  }

}
```




我的教学案例网站：
https://packdiy.com/

hostdare服务器入口：
[https://bill.hostdare.com/](https://bill.hostdare.com/aff.php?aff=4286)

hostinger域名入口：
[https://hostinger.com](https://hostinger.com?REFERRALCODE=TimVPS)



如果文字教程看不懂，也可以看我的视频教程。
 
#外贸独立站搭建
#跨境电商
#外贸服务器

