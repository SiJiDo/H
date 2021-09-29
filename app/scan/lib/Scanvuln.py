from celery import Celery
from sqlalchemy.sql.expression import false
from app.home.utils import *
from app.home.utils import *
import time 
import configparser
from threading import *
from app.scan.conn import dbconn
import queue
from threading import *

cfg = configparser.ConfigParser()
cfg.read('config.ini')

lock=Lock()

def scan_vuln(scanmethod_query, target_id, current_user):
    #初始化数据库连接
    conn,cursor = dbconn()
    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)

    #查询该目标的未扫描的域名
    sql = "SELECT * FROM Http WHERE http_target=%s"
    cursor.execute(sql,(target_id))
    http_query = cursor.fetchall()

    #初始化多线程
    thread_count = 10
    nuclei_queue = queue.Queue()

    #整理队列
    for nuclei_target in http_query:
        nuclei_queue.put(nuclei_target)

    #nuclei --多线程
    if(scanmethod_query[14] == True):
        github = ""
        daily = False
        # 使用多线程
        threads = []
        for i in range(0, thread_count):
            thread = tool_nuclei(nuclei_queue, task, daily, github, target_id, conn, cursor, current_user)
            thread.start()
            threads.append(thread)
        for j in threads:
            j.join()

    #nuclei 自定义
    if(scanmethod_query[15] == True):
        sql = "SELECT config_vuln_github FROM Sysconfig"
        cursor.execute(sql)
        result = cursor.fetchone()
        github = result[0]
        daily = False
        # 使用多线程
        threads = []
        for i in range(0, thread_count):
            thread = tool_nuclei(nuclei_queue, task, daily, github, target_id, conn, cursor, current_user)
            thread.start()
            threads.append(thread)
        for j in threads:
            j.join()
        
    #xray
    if(scanmethod_query[13] == True):
        tool_xray(task, http_query, conn, cursor)

    cursor.close()
    conn.close()
    return

class tool_nuclei(Thread):
    def __init__(self, nuclei_queue, task, daily, github, target_id, conn, cursor, current_user):
        Thread.__init__(self)
        self.queue = nuclei_queue
        self.task = task
        self.target_id = target_id
        self.cursor = cursor
        self.conn = conn
        self.current_user = current_user
        self.daily = daily
        self.github = github

    def run(self):
        queue = self.queue
        task = self.task
        target_id = self.target_id
        cursor = self.cursor
        conn = self.conn
        current_user = self.current_user
        daily = self.daily
        github = self.github

        while not queue.empty():
            target = queue.get()
            scan_target = target[1] + '://' + target[2]
            #发送celery
            vuln_scan = task.send_task('nuclei.run', args=(scan_target,daily,github,), queue='nuclei')

            while True:
                if vuln_scan.successful():
                    lock.acquire()
                    save_result(target, target_id, vuln_scan.result, cursor, conn, current_user)
                    lock.release()
                    break

# xray单线程
def tool_xray(task,http_query, conn, cursor):
    for target in http_query:
        scan_target = target[1] + '://' + target[2]
        httpx_list = []
        sql = "SELECT dir_base FROM Dirb WHERE dir_http = %s"
        cursor.execute(sql, (target[0]))
        result = cursor.fetchall()
        for r in result:
            httpx_list.append(r[0])

        xray_scan = task.send_task('xray.run', args=(scan_target,httpx_list,), queue='xray')
        
        starttime = time.time()
        nowtime = starttime

        while True:
            if xray_scan.successful():
                break
            if(nowtime > starttime + 630):
                task.control.revoke(xray_scan.id, terminate=True)
                print(scan_target + "目标超时")
                nowtime = time.time()
        

    return

def save_result(target, target_id, vuln_result, cursor, conn, current_user): 
    tool = vuln_result['tool']
    vuln_result = vuln_result['result']
    for result in vuln_result:
        sql = "SELECT * FROM Vuln WHERE vuln_mainkey=%s"
        count = cursor.execute(sql,((result['vuln_poc'] + result['vuln_info'])[:100]))

        if(count):
            sql = "UPDATE Vuln SET vuln_new=1 WHERE vuln_mainkey=%s"
            count = cursor.execute(sql,((result['vuln_poc'] + result['vuln_info'])[:100]))
            conn.commit()
        
        else:
            #入库
            print("vuln入库:" + result['vuln_info'])
            try:
                sql = "REPLACE INTO Vuln (vuln_mainkey, vuln_name,vuln_info,vuln_level,vuln_poc, vuln_http, vuln_target, vuln_time, vuln_user, vuln_tool,vuln_new) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',{});".format(
                    (result['vuln_poc'] + result['vuln_info'])[:100],
                    result['vuln_target'],
                    result['vuln_info'],
                    result['vuln_level'],
                    result['vuln_poc'],
                    target[0],
                    target_id,
                    time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())), 
                    str(current_user),
                    tool,
                    0,
                )
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)

    return