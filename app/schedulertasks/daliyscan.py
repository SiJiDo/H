import time
from celery import Celery
import configparser
import queue
from threading import *
from app.scan.conn import dbconn

cfg = configparser.ConfigParser()
cfg.read('config.ini')

lock=Lock()

def scan_daliy_vuln():
    print("进入了每日漏洞扫描模块")

    conn, cursor = dbconn()

    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)

    #更新nuclei的poc
    vuln_scan = task.send_task('nuclei.run', args=("",False,"",True,), queue='nuclei')
    while True:
        if vuln_scan.successful():
            break
    
    sql = "SELECT * FROM Target,Scanmethod WHERE target_method = Scanmethod.id AND scanmethod_nuclei = True";
    cursor.execute(sql)
    results = cursor.fetchall()
    vuln_taget = []
    for result in results:
        sql = "SELECT http_schema,http_name,http_target,http_user FROM Http WHERE http_target = %s";
        cursor.execute(sql,(result[0]))
        target_result = cursor.fetchall()
        for i in target_result:
            dic = {}
            dic['target'] = i[0] + "://" + i[1]
            dic['http_target'] = i[2] 
            dic['http_user'] = i[3]
            vuln_taget.append(dic)
        
    #初始化多线程
    thread_count = 10
    nuclei_queue = queue.Queue()

    #整理队列
    for nuclei_target in vuln_taget:
        nuclei_queue.put(nuclei_target)

    #nuclei --多线程
    github = ""
    daily = True
    # 使用多线程
    threads = []
    for i in range(0, thread_count):
        thread = tool_nuclei(nuclei_queue, task, daily, github, conn, cursor)
        thread.start()
        threads.append(thread)
    for j in threads:
        j.join()
        
    cursor.close()
    conn.close()

class tool_nuclei(Thread):
    def __init__(self, nuclei_queue, task, daily, github, conn, cursor):
        Thread.__init__(self)
        self.queue = nuclei_queue
        self.task = task
        self.cursor = cursor
        self.conn = conn
        self.daily = daily
        self.github = github

    def run(self):
        queue = self.queue
        task = self.task
        cursor = self.cursor
        conn = self.conn
        daily = self.daily
        github = self.github

        while not queue.empty():
            target = queue.get()
            scan_target = target['target']
            #发送celery
            vuln_scan = task.send_task('nuclei.run', args=(scan_target,daily,github,), queue='nuclei')

            while True:
                if vuln_scan.successful():
                    lock.acquire()
                    save_result(target, target['http_target'], vuln_scan.result, cursor, conn, target['http_user'])
                    lock.release()
                    break

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

if __name__ == '__main__':
    scan_daliy_vuln('127.0.0.1',3306, 'root', 'root', 'H')