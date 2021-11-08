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

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.nuclei', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target, flag=False, github=""):
    work_dir = FILEPATH + '/tools'
    out_file_name = '{}.txt'.format(time())
    result = []

    # 先更新
    if DEBUG == 'True':
        command = ['./nuclei_mac', '-ut', '-update']
    else:
        command = ['./nuclei', '-ut', '-update']
    try:
        sb = SubProcessSrc(command, cwd=work_dir).run()
    except:
        pass

    #周期扫描新poc
    if(flag == True):
        # 执行命令 ./nuclei -target target -t "nuclei-templates" -o 1.txt
        if DEBUG == 'True':
            command = ['./nuclei_mac', '-u', target, '-config', 'config_new.yaml', '-json', '-o', out_file_name]
        else:
            command = ['./nuclei', '-u', target, '-config', 'config_new.yaml', '-json', '-o', out_file_name]
    #自定义poc
    elif(github != ""):
        dir_name = github.split("/")[-1].split('.')[0]
        print(dir_name)
        try:
            #更新自定义的poc
            if(os.path.exists(work_dir + '/' + dir_name)):
                command = ['git', 'pull', github]
            else:
                command = ['git', 'clone', github]
                sb = SubProcessSrc(command, cwd=work_dir).run()
        except:
            pass
        if DEBUG == 'True':
            command = ['./nuclei_mac', '-u', target, '-severity','low,medium,high,critical', '-templates', dir_name, '-json', '-o', out_file_name]
        else:
            command = ['./nuclei', '-u', target, '-severity','low,medium,high,critical', '-templates', dir_name, '-json', '-o', out_file_name]

    else:
        # 执行命令 ./nuclei -target target -t "nuclei-templates" -o 1.txt
        if DEBUG == 'True':
            command = ['./nuclei_mac', '-u', target, '-config', 'config.yaml', '-json', '-o', out_file_name]
        else:
            command = ['./nuclei', '-u', target, '-config', 'config.yaml', '-json', '-o', out_file_name]
        
    sb = SubProcessSrc(command, cwd=work_dir).run()
    if sb['status'] == 0:
        result = send_info(sb, work_dir, out_file_name)

    return {'tool': 'nuclei', 'result': result}

def send_info(sb, work_dir, out_file_name):
    result = []
    # 运行成功，读取json数据返回
    with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
        vuln = f.readlines()
        for line in vuln:
            dic = {}
            try:
                dic['vuln_level'] = json.loads(line)['info']['severity']
                dic['vuln_poc'] = json.loads(line)['matched']
                dic['vuln_info'] = json.loads(line)['info']['name']
                dic['vuln_target'] = json.loads(line)['host']

                result.append(dic)

            except Exception as e:
                print(e)
    try:
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
    except:
        pass

    return result

if __name__ == '__main__':
    target = 'http://127.0.0.1:8081/'
    print(run(target, github=""))
