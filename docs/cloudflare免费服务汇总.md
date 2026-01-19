### Cloudflare免费服务汇总

第一：免费cdn/免费dns，无限流量

如何使用：将域名nameserver解析到cloudflare上自动使用,

橙色表示代理自动cdn，灰色表示仅dns无cdn

第二：workers和pages

用量点击workers和pages 右侧可以看到使用情况

workers可以创建100个，每天免费用量是10万次（所有workers共享）

pages则无限制，流量无限

第三：R2存储服务

左侧菜单，点击存储，点击R2

R2的价格政策：（free tier+价格）

https://developers.cloudflare.com/r2/pricing/

第四：D1数据库

左侧菜单，点击D1数据库，右侧看使用情况。

如果超量，免费版则停止服务，付费版则付费，

价格政策：

https://developers.cloudflare.com/d1/platform/pricing/

第五：Zero Trust

免费50个，比如网络连接 (Cloudflare Tunnel)： 完全免费且不限流量。你可以通过隧道将本地内网服务安全地暴露到公网，无需公网 IP 或配置路由器。

比如还有warp服务，免费额度也是50

第六：Turnstile

永久免费，最多创建20个组件

价格政策：

https://developers.cloudflare.com/turnstile/plans/
