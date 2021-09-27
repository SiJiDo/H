#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
import os
from time import time
import json
#from process import SubProcessSrc
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

app = Celery('hhsrc.massdns', broker=broker, backend=backend, )
app.config_from_object('config')

@app.task
def run(domain, wordlist = "words.txt"):
    work_dir = FILEPATH + '/tools'
    out_file_name = '{}_{}.json'.format(domain, time())
    # 执行命令 ./subfinder_mac -d example.com -json -o
    if DEBUG == 'True':
        command = ['./shuffledns_mac', '-d', domain, '-w', wordlist, '-r', "resolver.txt", '-o', out_file_name]
    else:
        command = ['./shuffledns', '-d', domain, '-w', wordlist, "-massdns", "./massdns", '-r', "resolver.txt", '-o', out_file_name]
    sb = SubProcessSrc(command, cwd=work_dir).run()
    result = []
    if sb['status'] == 0:
        # 运行成功，读取json数据返回
        with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
            path = f.readlines()
            for line in path:
                try:
                    url = line.split('\n')[0]
                    result.append(url)
                except Exception as e:
                    print(e)
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
        if(wordlist == 'words.txt'):
            return {'tool': 'shuffledns', 'result': result}
        else:
            return {'tool': 'second_shuffledns', 'result': result}

if __name__ == '__main__':
    print(run('oppo.com'))
