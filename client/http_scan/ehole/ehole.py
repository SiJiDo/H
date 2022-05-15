#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from time import time
import os
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

app = Celery('H.ehole', broker=broker, backend=backend, )
app.config_from_object('config')

@app.task
def run(target):
    #生成文件
    target_file = 'EHoletmp_{}.txt'.format(time())
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
        command = ['./Ehole_mac', '-l', target_file, '-json', out_file_name]
    else:
        command = ['./Ehole', '-l', target_file, '-json', out_file_name]
    result = []
    #整体抛出异常，以防httpx自身报错
    try:
        sb = SubProcessSrc(command, cwd=work_dir).run()
        if sb['status'] == 0:
            pass
            #运行成功，读取json数据返回
            with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
                url = f.readlines()
                for line in url:
                    #print(line)
                    dic = {}
                    try:
                        dic["http_name"] = json.loads(line)['url']
                        dic["http_finger"] = json.loads(line)['cms']
                    except:
                        dic["http_name"] = json.loads(line)['url']
                        dic["http_finger"] = "None"
                    if not dic["http_finger"]:
                        dic["http_finger"] = "None"
                    result.append(dic)
    except Exception as e:
        print(e)
    #当httpx出错，导致生成不了文件时，抛出异常
    try:
        os.system('rm -rf {}/{}'.format(work_dir, target_file))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
        os.system('rm -rf {}/{}'.format(work_dir, 'server.log'))
    except:
        pass
    return {'tool': 'EHole', 'result': result}


if __name__ == '__main__':
    print(run(["https://afgateway.vivo.com",
"https://fr.vivo.com",
"https://cloud.vivo.com",
"https://au.vivo.com",
"https://de.vivo.com",
"https://findphone.vivo.com",
"https://issue.dev.vivo.com",
"https://kernelapi.vivo.com",
"https://dev.vivo.com",
"https://b.vivo.com",
"https://browserproxy.vivo.com",
"https://as.vivo.com",
"https://iot.vivo.com",
"https://asia-exstatic.vivo.com",
"https://bhwkju.vivo.com",
"https://es.vivo.com",
"https://identity.vivo.com",
"https://75.vivo.com",
"https://asia-news-abroad.vivo.com",
"https://bbs.vivo.com",
"https://citrix.vivo.com",
"https://bs.vivo.com",
"https://passport.vivo.com",
"https://map.vivo.com",
"https://developer.vivo.com",
"https://pdm.vivo.com",
"https://opensource.vivo.com",
"https://asia-exstatic-vivofs.vivo.com",
"https://g.vivo.com",
"https://pc.vivo.coma",
"https://apps.vivo.com",
"https://93.vivo.com",
"https://106.vivo.com",
"https://meeting.vivo.com",
"https://ro.vivo.com",
"http://survey.vivo.com:8089",
"http://47.97.157.235:8888",
"http://61.178.209.31"]))
