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
        pass
        os.system('rm -rf {}/{}'.format(work_dir, target_file))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
    except:
        pass
    return {'tool': 'httpx', 'result': result}

if __name__ == '__main__':
    list2 = ['k3.vulnweb.com', 'home.vulnweb.com', 'ff9e0ea19912924.yl4.us-west-2.eks.vulnweb.com', 'sp.vulnweb.com', 'iimahd.vulnweb.com', '6-134.ap-northeast-2.compute.vulnweb.com', 'testphp.vulnweb.com', 'www.testasp.vulnweb.com', 'testaspnet.vulnweb.com', 'testasp.vulnweb.com', 'rest.vulnweb.com', 'localhost.vulnweb.com', 'rest.vulnweb.com:8080','testphp.vulnweb.com']
    print(run(list2))
