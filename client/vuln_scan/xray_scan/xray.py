#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/3 16:55
# @Author  : le31ei
# @File    : subfinder.py
from celery import Celery
import os
from time import sleep, time
import json

from process import SubProcessSrc
import subprocess

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.xray', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target, httpx= []):
    rad_work_dir = FILEPATH + '/tools/rad/'
    httpx_work_dir = FILEPATH + '/tools/httpx/'
    xray_host = "http://127.0.0.1:7777"
    httpx_list = httpx_work_dir + 'httpx_{}'.format(time())
    file = open(httpx_list, 'w');
    for tag in httpx:
        file.write(tag + '\n');
    file.close();

    # 先更新
    if DEBUG == 'True':
        command = './rad_mac -c rad_config.yml -t ' + target
        command2 = './rad_mac -c rad_config_moblie.yml -t ' + target
        command3 = './httpx_mac -http-proxy ' + xray_host +  ' -l ' + httpx_list
    else:
        command = './rad -c rad_config.yml -t ' + target
        command2 = './rad -c rad_config_moblie.yml -t ' + target
        command3 = './httpx -http-proxy ' + xray_host +  ' -l ' + httpx_list

    run_command(command, rad_work_dir)
    run_command(command2, rad_work_dir)
    run_command(command3, httpx_work_dir)
    try:
        os.system('rm -rf {}'.format(httpx_list))
    except:
        pass

    return "ok"

def run_command(command, rad_work_dir):

    cmd = subprocess.Popen(command, shell=True, cwd = rad_work_dir)
    #爬虫超过5分钟，自动杀死进程
    pid = str(cmd.pid)

    starttime = time()
    nowtime = starttime
    while True:
        try:
            ret = subprocess.Popen.poll(cmd)
            if ret == 0:
                break
            if(nowtime > starttime + 300):
                os.system("kill " + pid)    
                print("目标超时")
                break
            nowtime = time()
        except:
            break

    return "ok"

if __name__ == '__main__':
    target = 'http://bbs.vivo.com/'
    print(run(target, ))
