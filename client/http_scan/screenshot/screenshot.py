#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from time import time
from selenium import webdriver
from process import SubProcessSrc
from threading import *
from PIL import Image
import queue
import os
import base64

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.screenshot', broker=broker, backend=backend, )
app.config_from_object('config')

#使用多线程
class screenshot(Thread):
    def __init__(self, target_queue, result):
        Thread.__init__(self)
        self.queue = target_queue
        self.result = result

    def screen(self, target):
        if(DEBUG == 'True'):
            browser = webdriver.PhantomJS(executable_path='tools/phantomjs_mac')
        else:
            browser = webdriver.PhantomJS(executable_path='tools/phantomjs')
        try:
            work_dir = FILEPATH + '/tools'
            target_output_file = work_dir + '/' + 'screenshot_{}.png'.format(time())
            picture_url = target
            browser.maximize_window()
            browser.set_page_load_timeout(30)
            browser.get(picture_url)
            #截图#######################################
            browser.save_screenshot(target_output_file)
            print("%s：截图成功！！！" % picture_url)
            browser.quit()

            #调整分辨率
            im = Image.open(target_output_file)
            im = im.crop((0, 0, 1350, 768))
            type = im.format
            out = im.resize((300,150), Image.BILINEAR)
            out.save(target_output_file, type)

            #图片转base64
            base64_data = ""
            with open(target_output_file, 'rb') as f:
                base64_data = str(base64.b64encode(f.read()), encoding='utf-8')
            os.system('rm -rf {}'.format(target_output_file))
            os.system('rm -rf ghostdriver.log')
            return base64_data

        except BaseException as msg:
            browser.close()
            print(msg)

        return "None"


    def run(self):
        queue = self.queue
        result = self.result
        while not queue.empty():
            try:
                info = {}
                
                screen_target = queue.get()
                screen_base64 = self.screen(screen_target)
                info['http'] = screen_target
                info['screen_base64'] = screen_base64
                result.append(info)
            except Exception as e:
                print(e)
        return

@app.task
def run(target_list):
    result = []
    thread_count = 5
    target_queue = queue.Queue()
    for target in target_list:
        target_queue.put(target)

    # 使用多线程
    threads = []
    for i in range(0, thread_count):
        thread = screenshot(target_queue, result)
        thread.start()
        threads.append(thread)

    for j in threads:
        j.join()
    os.system("ps -ef |grep phantomjs |awk '{print $2}'|xargs kill -9")
    return {'tool': 'screenshot', 'result': result}


if __name__ == '__main__':
    print(run(["https://pop.oppo.com"]))
