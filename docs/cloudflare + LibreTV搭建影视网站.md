> 基于Cloudflare + LibreTV搭建个人影视站。


### 第一步：准备源码与 GitHub 同步

https://github.com/LibreSpark/LibreTV

点击fork 克隆一份属于你自己的仓库

### 第二步：Cloudflare Pages 零成本部署

- 登录 Cloudflare，进入 Pages。
- 连接你的 GitHub 账号，授权仓库访问。
- 选择刚刚 Fork 的 LibreTV 项目。
- 构建设置（Build Settings）
- 点击部署，等到出现 “Success”。

### 第三步：一键绑定自定义域名

- 在 Cloudflare Pages 的项目后台，点击 “自定义域 (Custom Domains)” 选项卡。
- 点击 “设置自定义域”。
- 输入你已经在 CF 托管的域名（或二级域名，比如 tv.yourdomain.com）。
- 根据提示激活域

### 第四步：配置 API 搜索接口

点击右上角 设置图标，找到自定义api的入口，填写。



