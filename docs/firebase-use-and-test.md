> 本文分享谷歌Firebase免费主机服务的用法、测速


### 基本用法

- 第一步：安装node [下载地址](https://nodejs.org/zh-cn/download)
- 第二步：安装firebase： ```npm install -g firebase-tools```
- 第三步：新建firebase项目
- 第四步：firebase登录（注）
- 第五步：firebase初始化
- 第六步：firebase部署

常用命令：
```
登录
firebase login
初始化
firebase init hosting
来查看可用项目 ID
firebase projects:list
切换项目
firebase use <项目ID>
查看当前active项目（不带参数）
firebase use
部署
firebase deploy
登出
firebase logout
```

firebase登录失败怎么办？
```
firebase login登录失败，解决办法：设置proxy
先在cmd命令行中这样: 
set http_proxy=http://127.0.0.1:10808
set https_proxy=http://127.0.0.1:10808
set NODE_TLS_REJECT_UNAUTHORIZED=0
设置系统代理，然后设置npm的代理
npm config set proxy http://127.0.0.1:10808
```

### 测速

![](https://github.com/geeeeeeeek/side_pro/blob/master/docs/raw/ping.jpg?raw=true)


### 对比Cloudflare

 

| 对比维度 | ☁️ Firebase Hosting | 🌩️ Cloudflare Pages | Tim建议 |
| :--- | :--- | :--- | :--- |
| **底层网络 (CDN)** | Google 全球骨干网 | Cloudflare 全球 Anycast  | Firebase 在部分海外地区加载极快；CF 国内部分地区可能会被阻断或减速。 |
| **免费额度 (Free Tier)** | **10 GB 存储** / **10 GB 月流量** | 流量无限制 / 每月 500 次免费构建 | Firebase 流量超标停用；CF 随便用。 |
| **部署方式 (Deployment)** | 本地命令行 (CLI) `firebase deploy` | 关联 GitHub 全自动构建 (CI/CD) | Firebase 适合爱敲命令行的全栈极客；CF 适合不懂代码、喜欢一键拉取代码的小白。 |
| **生态扩展能力** | 极强 (自带数据库、认证、云函数) | 较强 (Workers、D1 数据库) | 如果你的副业网站需要用户登录、存数据，选Firebase；纯静态博客/工具站选 CF。 |
| **国内访问友好度** | `web.app` 二级域名间歇污染 (需绑自定义域名) | `pages.dev` 二级域名间歇性被阻断 | 无论用哪个，**做 AdSense 副业都必须绑定独立域名！** |























