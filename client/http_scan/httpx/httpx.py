# -*- coding: utf-8 -*-
from celery import Celery
import os
from time import time
import json

from process import SubProcessSrc

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.httpx', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target):
    #生成文件
    target_file = 'httpxtmp_{}.txt'.format(time())
    file = open(FILEPATH + '/tools/' + target_file, 'w');
    for tag in target:
        file.write(tag + '\n');
    file.close();

    work_dir = FILEPATH + '/tools'
    out_file_name = '{}_{}.json'.format(target_file, time())
    # 执行命令 ./httpx_mac -l vivo.com.txt -cdn -json -follow-host-redirects -o 111.json
    if DEBUG == 'True':
        # command = ['whoami']
        #./httpx_mac -l vivo.com.txt -cdn -json -follow-host-redirects -o 111.json
        command = ['./httpx_mac', '-l', target_file, '-follow-host-redirects' , '-json', '-o', out_file_name]
    else:
        command = ['./httpx', '-l', target_file, '-follow-host-redirects' , '-json', '-o', out_file_name]
    result = []
    #整体抛出异常，以防httpx自身报错
    try:
        sb = SubProcessSrc(command, cwd=work_dir).run()
        if sb['status'] == 0:
            # 运行成功，读取json数据返回
            with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
                url = f.readlines()
                for line in url:
                    #print(line)
                    dic = {}
                    try:
                        dic["url"] = json.loads(line)['url']
                        dic["content-length"] = json.loads(line)['content-length']
                        dic["status-code"] = json.loads(line)['status-code']
                        dic["title"] = json.loads(line)['title']
                    except:
                        dic["url"] = json.loads(line)['url']
                        dic["content-length"] = ""
                        dic["status-code"] = json.loads(line)['status-code']
                        dic["title"] = ""
                    result.append(dic)
    except Exception as e:
        print(e)
    #当httpx出错，导致生成不了文件时，抛出异常
    try:
        os.system('rm -rf {}/{}'.format(work_dir, target_file))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
    except:
        pass
    return {'tool': 'httpx', 'result': result}

if __name__ == '__main__':
    list2 = ['sdp.vivo.com', 'bs.vivo.com', 'err.up.vivo.com', 'vds.vivo.com', 'zhushou.vivo.com', 'passport.vivo.com', 'global.vivo.com', 'findphone.vivo.com', 'ru.vivo.com', 'internetgratis.vivo.com', 'hr.vivo.com', 'browserproxy.vivo.com', 'in-ali-cname-www.vivo.com', 'www.ru.vivo.com', 'as.vivo.com', 'cloud.vivo.com', 'visionplus.vivo.com', 'zs.vivo.com', 'zhaopin.vivo.com', 'asia-news-abroad.vivo.com', 'vivo.com', 'tianma-prd-in.vivo.com', 'shop.vivo.com', 'issue.dev.vivo.com', 'easyshare.vivo.com', 'homepagestatic.vivo.com', 'tech.vivo.com', 'shgj.vivo.com', 'in-exstatic-vivofs.vivo.com', 'asia-exstatic.vivo.com', 'www.vivo.com', 'sg-exstpay.vivo.com', 'in-ali-browserproxy-cname.vivo.com', 'bhwkju.vivo.com', 'es.vivo.com', 'homepage.vivo.com', 'asia-exstatic-vivofs.vivo.com', 'medialive.vivo.com', 'mshop.vivo.com']
    print(run(list2))
