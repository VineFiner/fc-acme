# 使用 acme 进行证书申请

- 下载并安装

```
git clone https://github.com/acmesh-official/acme.sh.git
cd acme.sh
./acme.sh --install  \
--home ~/myacme \
--config-home ~/myacme/data \
--cert-home  ~/mycerts \
--accountemail  "my@example.com" \
--accountkey  ~/myaccount.key \
--accountconf ~/myaccount.conf \
--useragent  "this is my client."
```
- 颁发证书

```
./acme.sh  \
  --issue \
  --server letsencrypt \
  --dns dns_ali \
  -d aaa.com \
  -d *.aaa.com \
  -d bbb.com \
  -d *.bbb.com \
  -d ccc.com \
  -d *.ccc.com \
  -k 2048
```

- 输出证书

```
./acme.sh  \
  --install-cert \
  -d aaa.com \
  -d *.aaa.com \
  --key-file /nginx/aaa_com.key  \
  --fullchain-file /nginx/aaa_com.pem
```

## 使用云函数部署

```
s deploy -t ./s.yaml -a fc-access --use-local -y
```
> 需要在 `invoke-acme` 函数配置 DNS 平台秘钥 https://www.ioiox.com/archives/87.html

> 我们需要在 定时触发器添加域名 `aaa.com`