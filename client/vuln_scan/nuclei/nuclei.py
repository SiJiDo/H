#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 16:55
# @Author  : le31ei
# @File    : subfinder.py
from celery import Celery
import os
from time import time
import json

from process import SubProcessSrc
import subprocess
from urllib.parse import urlparse

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://hhsrc:hhsrc@127.0.0.1:5672/hhsrc_broker'
    backend = 'amqp://hhsrc:hhsrc@127.0.0.1:5672/hhsrc_backend'

app = Celery('hhsrc.nuclei', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target):
    print("-------------------调用nuclei组件:" + target + "--------------------")
    work_dir = FILEPATH + '/tools'
    nucelei_tmp = work_dir + '/nuclei-templates'
    out_file_name = '{}.txt'.format(time())
    result = []

    # 先更新
    command = ['git', 'pull']
    try:
        sb = SubProcessSrc(command, cwd=nucelei_tmp).run()
    except:
        pass
    # 执行命令 ./nuclei -target target -t "nuclei-templates" -o 1.txt
    if DEBUG == 'True':
        command = ['./nuclei_mac', '-target', target, '-no-color', '-silent', '-config', 'config.yaml']
    else:
        command = ['./nuclei', '-target', target, '-no-color', '-silent', '-config', 'config.yaml']
    sb = SubProcessSrc(command, cwd=work_dir, stdout=subprocess.PIPE).run()
    if sb['status'] == 0:
        for r in sb['result']:
            try:
                dic = {}
                dic['target'] = ""
                dic['vuln_level'] = ""
                dic['vuln_info'] = ""
                dic['vuln_path'] = ""
                line = r.decode("utf-8")
                url = line.split('] ')[-1].split('\n')[0].split(" [")[0]
                if("://" not in url):
                    url = "http://" + url
                urlres = urlparse(url)
                dic['target'] = urlres.scheme + "://" + urlres.netloc
                dic['vuln_level'] = line.split('] ')[-2].split('[')[-1]
                dic['vuln_info'] = line.split('[')[2].split(']')[0]
                dic['vuln_path'] = line.split('] ')[-1].split('\n')[0]
                result.append(dic)
            except Exception as e:
                print(e)
    return {'tool': 'nuclei', 'result': result}

if __name__ == '__main__':
    list2 = 'https://asia-exstatic.vivo.com'
    print(run(list2))
