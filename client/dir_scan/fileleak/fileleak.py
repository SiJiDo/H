#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
import os
from time import time
import json

from process import SubProcessSrc
from urllib.parse import urlparse

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.fileleak', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target, dic='top100'):

    work_dir = FILEPATH + '/tools'
    out_file_name = '{}.txt'.format(time())

    wordlist = 'dic/dic_top1000.txt'
    if(dic == 'top100'):
        wordlist = 'dic/dic_top100.txt'
    if(dic == 'top1000'):
        wordlist = 'dic/dic_top1000.txt'
    if(dic == 'top7000'):
        wordlist = 'dic/dic_top7000.txt'

    # 执行命令 ./fileleak.py --target http://mi0.xyz --output 1234.txt
    if DEBUG == 'True':
        command = ['python3', 'fileleak.py', '--target', target, '--dict', wordlist, '--output', out_file_name]
    else:
        command = ['python3', 'fileleak.py', '--target', target, '--dict', wordlist, '--output', out_file_name]
    result = []
    try:
        sb = SubProcessSrc(command, cwd=work_dir).run()
        if sb['status'] == 0:
            # 运行成功，读取json数据返回
            with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
                path = f.readlines()
                for line in path:
                    try:
                        dic = {}
                        url = line.split(']')[-1].split('\n')[0]
                        urlres = urlparse(url)
                        dic["host"] = urlres.scheme + "://" + urlres.netloc
                        dic["path"] = urlres.path
                        dic["content-length"] = line.split('[')[-1].split(']')[0]
                        dic["title"] = line.split('[',2)[2].split(']')[0]
                        dic["status-code"] = line.split('[')[1].split(']')[0]
                        result.append(dic)
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)

    try:
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
    except:
        pass
    return {'tool': 'fileleak', 'result': result}

if __name__ == '__main__':
    target = 'https://es.vivo.com/'
    print(run(target))
