#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
import time
import os
import json
from tools.tianyan_beian import  domainget
from subprocess import Popen

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.icpget', broker=broker, backend=backend, )
app.config_from_object('config')

@app.task
def run(company, cookie):
    workdir = FILEPATH + '/tools/'
    output_file1 = 'output_{}.txt'.format(time.time())
    output_file2 = 'output_{}.txt'.format(time.time())
    if DEBUG == 'True':
        command = './cSubsidiary_mac -n "{}" -c "{}" -p 90 > {}'.format(company,cookie,output_file1)
    else:
        command = './cSubsidiary -n "{}" -c "{}" -p 90 > {}'.format(company,cookie,output_file1)
    cmd = Popen(command,cwd=workdir, shell=True)
    while 1:
        ret = Popen.poll(cmd)
        if ret == 0:
            break

    f = open(workdir + output_file1, 'r')
    tmp = []
    for line in f.readlines():
        line = line.strip()
        if("www.tianyancha.com/company/" in line):
            if("的子公司" in line):
                tmp.append((line.split("/company/")[1].split(" 的子公司")[0], company))
            else:
                tmp.append((line.split("/company/")[1].split("\t")[0], line.split("/company/")[1].split("\t")[1]))

    try:
        os.system("rm -rf {}".format(workdir + output_file1))
    except:
        pass
    
    content = []
    all = []
    for i in tmp:
        dic = {}
        dic['name'] = i[1]
        dic['domain'] = domainget(i[0], cookie)
        content.append(dic)
        all = all + dic['domain']

    return content, all


if __name__ == '__main__':
    pass