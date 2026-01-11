
> 本文对vultr最便宜的服务器做一次评测，很多人或许都知道，vultr服务器最大的优点就是按小时计费，用多少付多少，再就是低流量费，每月有2TB的流量赠送，然后支付方式也支持支付宝支付。 最便宜的服务器就是2.5美元/月，一台是3.5美元/月。我个人感觉性价比最高的是3.5美元的这台，因为它支持ipv4。虽然2.5美元的这台更便宜，但是它不支持ipv4，如果要单独开通ipv4 还需要多付费，综合算下来呢，还不如3.5美元的这台便宜。所以我用这台3.5美元的这台做测试。

### 评测工具

- ping.pe
- tcptest
- goecs
- https://geotraceroute.com/


### 注意事项

- 赠送额度
- 可以使用多少次

### goecs安装步骤

```
安装
export noninteractive=true && curl -L https://cdn.spiritlhl.net/https://raw.githubusercontent.com/oneclickvirt/ecs/master/goecs.sh -o goecs.sh && chmod +x goecs.sh && ./goecs.sh env && ./goecs.sh install
使用
goecs
```
