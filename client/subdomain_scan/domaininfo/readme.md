# domaininfo
> 用于查询域名dns记录
### input
```
www.qq.com
```
### output
```
# 查询结果如下
{'domain': 'www.qq.com', 'type': 'CNAME', 'record': ['ins-r23tsuuf.ias.tencent-cloud.net'], 'ips': ['121.14.77.221', '121.14.77.201']}
# 传入服务端结果如下
{'tool': 'domaininfo', 'result': {'domain': 'www.qq.com', 'type': 'CNAME', 'record': ['ins-r23tsuuf.ias.tencent-cloud.net'], 'ips': ['121.14.77.221', '121.14.77.201']}}
```