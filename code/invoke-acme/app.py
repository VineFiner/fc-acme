from flask import Flask, Response
from flask import request
import os
import json

REQUEST_ID_HEADER = 'x-fc-request-id'

app = Flask(__name__)

# 安装 acme
@app.route('/initialize', methods=['POST'])
def init_invoke():
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Initialize Start RequestId: " + rid)
    # do your things
    if not os.path.exists("/mnt/auto/acmenas"):
        # 下载仓库
        os.system(
            "git clone https://github.com/acmesh-official/acme.sh.git")
        # 装载
        os.system(
            "cd acme.sh && bash acme.sh --install  \
            --home /mnt/auto/acmenas \
            --accountemail  \"my@example.com\" \
            --nocron")
    if not os.path.exists("/mnt/auto/nginx"):
        # 证书输出位置
        os.system("mkdir -p /mnt/auto/nginx")
    print("FC Initialize End RequestId: " + rid)
    return "OK", 200, []

# 默认路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world(path):
    rid = request.headers.get(REQUEST_ID_HEADER)
    print("FC Invoke Start RequestId: " + rid)
    data = request.stream.read()
    print("Path: " + path)
    print("Data: " + str(data))
    print("FC Invoke End RequestId: " + rid)
    return "Hello, World!"

# 颁发证书
@app.route('/invoke', methods=['POST'])
def invoke_acme():
    body = request.get_data()
    if body is None or body == "":
        return "not found post body", 400, []
    info = json.loads(body)
    domain = info["domain"]
    print(domain)
    # 获取 DNS 平台, 默认 dns_ali
    if "DNS_TYPE" in os.environ:
        dnstype = os.environ['DNS_TYPE']
    else:
        dnstype = "dns_ali"
        # 设置域名服务器环境变量
        # os.environ["Ali_Key"]=''
        # os.environ["Ali_Secret"]=''
    issuestring = "/mnt/auto/acmenas/acme.sh \
            --issue \
            --server letsencrypt \
            --dns {0} \
            -d {1} \
            -k 2048"
    print(issuestring.format(dnstype, domain))
    # 颁发证书
    os.system(issuestring.format(dnstype, domain))
    installstring = "/mnt/auto/acmenas/acme.sh \
        --install-cert \
        -d {0} \
        --key-file /mnt/auto/nginx/{1}_key.pem  \
        --fullchain-file /mnt/auto/nginx/{2}_cert.pem \
        "
    print(installstring.format(domain, domain, domain))
    # 导出证书
    os.system(installstring.format(domain, domain, domain))
    # 证书信息
    with open(os.path.join('/mnt/auto/nginx', '{0}_key.pem'.format(domain))) as keyfile:
        key = keyfile.read()
        keyfile.close()
    with open(os.path.join('/mnt/auto/nginx', '{0}_cert.pem'.format(domain))) as certfile:
        cert = certfile.read()
        certfile.close()
    acmedic = {
        "key": str(key),
        "cert": str(cert)
    }
    return Response(json.dumps(acmedic), mimetype='application/json')

# main 函数
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
