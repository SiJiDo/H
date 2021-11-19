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

app = Celery('H.jsfinder', broker=broker, backend=backend, )
app.config_from_object('config')


@app.task
def run(target):

    work_dir = FILEPATH + '/tools'
    out_file_name = 'jsfinder_{}.txt'.format(time())
    out_file_name1 = 'jsfinder_{}.txt'.format(time())
    out_file_name2 = 'httpx_{}.txt'.format(time())
    out_file_name3 = 'httpx_{}.txt'.format(time())

    # 执行命令
    if DEBUG == 'True':
        command = ['python3', 'JSFinder.py', '-u', target, '-ou', out_file_name]
        command1 = ['python3', 'JSFinder_moblie.py', '-u', target, '-ou', out_file_name1]
        command2 = ['./httpx_mac', '-l', out_file_name, '-follow-host-redirects' , '-json', '-o', out_file_name2]
        command3 = ['./httpx_mac', '-l', out_file_name1, '-follow-host-redirects' , '-json', '-o', out_file_name3]
    else:
        command = ['python3', 'JSFinder.py', '-u', target, '-ou', out_file_name]
        command1 = ['python3', 'JSFinder_moblie.py', '-u', target, '-ou', out_file_name1]
        command2 = ['./httpx', '-l', out_file_name, '-follow-host-redirects' , '-json', '-o', out_file_name2]
        command3 = ['./httpx', '-l', out_file_name1, '-follow-host-redirects' , '-json', '-o', out_file_name3, '-H', 'User-Agent: Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36', '-random-agent=False' ]
    result = []

    result = tool(command, command2, work_dir, out_file_name2, target)
    result = result + tool(command1, command3, work_dir, out_file_name3 , target)
    try:
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name1))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name2))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name3))
    except:
        pass
    return {'tool': 'jsfinder', 'result': result}

def tool(command, command2, work_dir, out_file_name, target):
    result = []
    sb = SubProcessSrc(command, cwd=work_dir).run()
    if sb['status'] == 0:      
        # 运行成功，读取数据
        sb = SubProcessSrc(command2, cwd=work_dir).run()
        if sb['status'] == 0:
            try:
                with open('{}/{}'.format(work_dir, out_file_name), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        flag = False
                        for qc in result:
                            if (json.loads(line)['path'] == qc['path']):
                                flag = True
                                break
                        if(target.split("://")[1] in json.loads(line)['url'] and flag == False and json.loads(line)['status-code'] in [200,500,403,503] and 'javascript' not in json.loads(line)['content-type'] and 'image' not in json.loads(line)['content-type']): 
                            dic={"host":"", "path":"", "content-length":"", "title":"", "status-code":""}
                            try:
                                url = json.loads(line)['url']
                                urlres = urlparse(url)
                                dic["host"] = urlres.scheme + "://" + urlres.netloc
                                dic["path"] = urlres.path
                                dic["content-length"] = json.loads(line)['content-length']
                                dic["title"] = json.loads(line)['title']  + "(moblie)" if '-H' in command2 else json.loads(line)['title']
                                dic["status-code"] = json.loads(line)['status-code']
                                result.append(dic)
                            except:
                                url = json.loads(line)['url'] + '(moblie)'
                                urlres = urlparse(url)
                                dic["host"] = urlres.scheme + "://" + urlres.netloc
                                dic["path"] = urlres.path
                                dic["content-length"] = ""
                                dic["title"] = ""
                                dic["status-code"] = json.loads(line)['status-code']
                                result.append(dic)
            except:
                pass
    return result

if __name__ == '__main__':
    target = 'https://wlmkids.com:443'
    print(run(target))
