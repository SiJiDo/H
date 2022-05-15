#!/usr/bin/env python
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

app = Celery('H.fscan', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target, port, flag=False, github="", update = False):
    work_dir = FILEPATH + '/tools'
    out_file_name = '{}.txt'.format(time())
    result = []

    if DEBUG == 'True':
        command = ['./fscan_mac', '-np', '-h', target, '-p', port , '-o', out_file_name]
    else:
        command = ['./fscan', '-np', '-h', target, '-p', port , '-o', out_file_name]

        
    sb = SubProcessSrc(command, cwd=work_dir).run()
    if sb['status'] == 0:
        result = send_info(sb, work_dir, out_file_name, target)

    return {'tool': 'fscan', 'result': result}

def send_info(sb, work_dir, out_file_name, target):
    result = []
    # 运行成功，读取json数据返回
    try:
        with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
            vuln = f.readlines()
            for line in vuln:
                if("[+]" not in line):
                    continue
                dic = {}
                dic['vuln_level'] = "fscan"
                dic['vuln_poc'] = "详细见fscan的poc文件"
                dic['vuln_info'] = line.strip()
                dic['vuln_target'] = target

                result.append(dic)

    except Exception as e:
        print(e)
    try:
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
    except:
        pass

    return result

if __name__ == '__main__':
    target = '139.159.159.70'
    port = '3306,80,6379,8080,5005'
    print(run(target, port))
