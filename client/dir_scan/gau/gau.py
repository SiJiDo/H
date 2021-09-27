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

app = Celery('H.gau', broker=broker, backend=backend, )
app.config_from_object('config')

@app.task
def run(target):

    work_dir = FILEPATH + '/tools'
    out_file_name = 'gau_{}.txt'.format(time())
    tmp_file_name = 'tmp_{}.txt'.format(time())
    tmp_file_name_2 = 'tmp2_{}.txt'.format(time())
    out_file_name2 = 'httpx_{}.txt'.format(time())

    # 执行命令 ./gau -o 1.txt -random-agent -b jpg,png,gif www.jd.com
    if DEBUG == 'True':
        command = ['./gau_mac', '-o', out_file_name, '-b', 'jpg,png,gif,html', target]
        command1 = ['sort', '-u', out_file_name, '-o', tmp_file_name]
        command2 = ['./httpx_mac', '-l', tmp_file_name, '-follow-host-redirects' , '-json', '-o', out_file_name2]
    else:
        command = ['./gau', '-o', out_file_name,  '-b', 'jpg,png,gif,html', target]
        command1 = ['sort', '-u', out_file_name, '-o', tmp_file_name]
        command2 = ['./httpx', '-l', tmp_file_name_2, '-follow-host-redirects' , '-json', '-o', out_file_name2]
        
    result = []
    tmp = []
    tmp2 = []
    try:
        sb = SubProcessSrc(command, cwd=work_dir).run()
        if sb['status'] == 0:
            sb = SubProcessSrc(command1, cwd=work_dir).run()
            if sb['status'] == 0:
                with open('{}/{}'.format(work_dir, tmp_file_name), 'r') as f:
                    tmp = f.readlines()
                #去重url
                for t in tmp:
                    t = t.split('\n')[0]
                    t2 = t.split('?')[0]
                    if(t2 not in tmp2):
                        tmp2.append(t)
                    
            file = open(FILEPATH + '/tools/' + tmp_file_name_2, 'w');
            for tag in tmp2:
                file.write(tag + '\n')
            file.close()

            sb = SubProcessSrc(command2, cwd=work_dir).run()
            if sb['status'] == 0:
                with open('{}/{}'.format(work_dir, out_file_name2), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        flag = False
                        for qc in result:
                            if (json.loads(line)['path'] == qc['path']):
                                flag = True
                                break
                        if(target.split("://")[1] in json.loads(line)['url'] and flag == False and json.loads(line)['status-code'] in [200,500,403,503] and 'javascript' not in json.loads(line)['content-type'] and 'image' not in json.loads(line)['content-type']): 
                            dic={}
                            try:
                                url = json.loads(line)['url']
                                urlres = urlparse(url)
                                dic["host"] = urlres.scheme + "://" + urlres.netloc
                                dic["path"] = urlres.path
                                dic["content-length"] = json.loads(line)['content-length']
                                dic["title"] = json.loads(line)['title']
                                dic["status-code"] = json.loads(line)['status-code']
                                result.append(dic)
                            except:
                                try:
                                    url = json.loads(line)['url']
                                    urlres = urlparse(url)
                                    dic["host"] = urlres.scheme + "://" + urlres.netloc
                                    dic["path"] = urlres.path
                                    dic["content-length"] = ""
                                    dic["title"] = ""
                                    dic["status-code"] = json.loads(line)['status-code']
                                    result.append(dic)
                                except Exception as e:
                                    print(e)
    except Exception as e:
        print(e)

    try:
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name))
        os.system('rm -rf {}/{}'.format(work_dir, tmp_file_name))
        os.system('rm -rf {}/{}'.format(work_dir, tmp_file_name_2))
        os.system('rm -rf {}/{}'.format(work_dir, out_file_name2))
    except:
        pass

    return {'tool': 'gau', 'result': result}

if __name__ == '__main__':
    target = 'https://www.vivo.com'
    print(run(target))
