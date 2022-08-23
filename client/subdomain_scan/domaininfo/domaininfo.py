#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
import os
from time import time
import json
from threading import *
import queue
import dns.resolver

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

if 'DEBUG' in os.environ and os.environ['DEBUG'] == 'False':
    broker = os.environ['BROKER']
    backend = os.environ['BACKEND']
    DEBUG = "False"
else:
    DEBUG = "True"
    broker = 'amqp://guest:guest@127.0.0.1:5672/H_broker'
    backend = 'amqp://guest:guest@127.0.0.1:5672/H_backend'

app = Celery('H.domaininfo', broker=broker, backend=backend, )
app.config_from_object('config')

@app.task
def run(domain_list):
    result = []
    thread_count = 64
    domain_queue = queue.Queue()
    for domain in domain_list:
        domain_queue.put(domain)

    # 使用多线程
    threads = []
    for i in range(0, thread_count):
        thread = domaininfo(domain_queue, result)
        thread.start()
        threads.append(thread)

    for j in threads:
        j.join()
    return {'tool': 'domaininfo', 'result': result}

#使用多线程
class domaininfo(Thread):
    def __init__(self, domain_queue, result):
        Thread.__init__(self)
        self.queue = domain_queue
        self.result = result

    ### func:get_ip and func:get_cname
    def get_ip(self, domain, log_flag = True):
        domain = domain.strip()
        ips = []
        try:
            answers = dns.resolver.resolve(domain, 'A')
            for rdata in answers:
                ips.append(rdata.address)
        except dns.resolver.NXDOMAIN as e:
            if log_flag:
                print("{} {}".format(domain, e))

        except Exception as e:
            if log_flag:
                print("{} {}".format(domain, e))
        return ips

    def get_cname(self, domain, log_flag = True):
        cnames = []
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            for rdata in answers:
                cnames.append(str(rdata.target).strip(".").lower())
        except dns.resolver.NoAnswer as e:
            if log_flag:
                print(e)
        except Exception as e:
            if log_flag:
                print("{} {}".format(domain, e))
        return cnames

    def run(self):
        queue = self.queue
        result = self.result
        while not queue.empty():
            try:
                domain = queue.get()
                ips = self.get_ip(domain)
                if not ips:
                    result.append({})
                cnames = self.get_cname(domain, False)
                info = {
                    "domain": domain,
                    "type": "A",
                    "record": ips,
                    "ips": ips
                }
                if cnames:
                    info["type"] = 'CNAME'
                    info["record"] = cnames
                result.append(info)
            except:
                pass
                #print("[-]host unknow")

        return


if __name__ == '__main__':
    print(run(["wave.neutrogena.com.cn www.babysleep.com.cn www.cleanandclear.com.cn www.dabao.com.cn www.johnsonsbaby.com.cn"]))
