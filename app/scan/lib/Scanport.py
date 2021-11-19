from celery import Celery
from app.home.utils import *
import time 
import configparser
import queue
from threading import *
from app.scan.conn import dbconn

cfg = configparser.ConfigParser()
cfg.read('config.ini')

lock=Lock()

def scan_port(scanmethod_query, target_id, current_user):
    #初始化数据库连接
    conn,cursor = dbconn()
    info = "target id:{} ---- 开始收集端口".format(target_id)
    sql = "INSERT INTO Runlog(log_info, log_time) VALUE('{}', '{}')".format(info, str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))))
    cursor.execute(sql)
    conn.commit()

    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)


    if(scanmethod_query[4] == False):
        return
    if(scanmethod_query[5] == 'deafult'):
        portlist = scanmethod_query[6]
    else:
        portlist = scanmethod_query[5]

    #查询该目标的未扫描的域名
    sql = "SELECT * FROM Subdomain where subdomain_target=%s"
    cursor.execute(sql,(target_id))
    subdomain_query = cursor.fetchall()

    #初始化多线程
    thread_count = 10
    port_queue = queue.Queue()
    #开始扫描
    for subdomain_info in subdomain_query:
        #排除多个ip解析情况，该情况大概率是cdn
        if(',' in subdomain_info[2] or '' == subdomain_info[2]):
            continue
        port_queue.put(subdomain_info)

    # 使用多线程
    threads = []
    for i in range(0, thread_count):
        thread = portscan(port_queue, portlist, task, target_id, cursor, conn, current_user )
        thread.start()
        threads.append(thread)
    for j in threads:
        j.join()

    cursor.close()
    conn.close()
    
    return

#使用多线程
class portscan(Thread):
    def __init__(self, port_queue, config, task, target_id, cursor, conn, current_user):
        Thread.__init__(self)
        self.queue = port_queue
        self.config = config
        self.task = task
        self.target_id = target_id
        self.cursor = cursor
        self.conn = conn
        self.current_user = current_user

    def run(self):
        queue = self.queue
        config = self.config
        task = self.task
        target_id = self.target_id
        cursor = self.cursor
        conn = self.conn
        current_user = self.current_user

        while not queue.empty():
            try:
                subdomain_info = queue.get()
                target = subdomain_info[2]
                #发送celery
                #naabu + nmap
                naabu_scan = task.send_task('naabu.run', args=(target, config), queue='naabu')
                while True:
                    if naabu_scan.successful():
                        try:
                            lock.acquire()
                            save_result(subdomain_info, target_id, naabu_scan.result['result'],cursor,conn, current_user)
                            lock.release()
                            break
                        except Exception as e:
                            print(e)
                            break
            except:
                pass
                #print("[-]host unknow")

        return

def save_result(subdomain_info, target_id, port_result,cursor, conn, current_user):  
    print("--------------------存储端口数据处-------------------------")
    print(port_result)
    if(len(port_result) > 50):
        return 
        
    for result in port_result:
        #去重,port比较特殊需要2个字段才能判断是否重复，因此需要进行查询
        sql = "SELECT * from Port WHERE port_ip =%s and port_port = %s"
        port_count = cursor.execute(sql,(result['ip'],str(result['port'])))
        if(port_count > 0):
            sql = "SELECT * from Port WHERE port_ip ='{}' AND port_port = '{}'  AND port_time like '%{}%'".format(result['ip'],str(result['port']),time.strftime('%Y-%m-%d', time.localtime(time.time())))
            if(cursor.execute(sql) == 0):
                sql = "UPDATE Port SET port_new={}  WHERE port_ip='{}' AND port_port='{}'".format(
                    1,
                    result['ip'],
                    str(result['port']),
                )
                cursor.execute(sql)
                conn.commit()
            continue 
        #存储数据
        sql = "SELECT subdomain_name from Subdomain WHERE id=%s"
        cursor.execute(sql,(subdomain_info[0]))
        host = cursor.fetchone()[0]
        print("开始端口入库:" + host + ":" + str(result['port']))
        #入库
        sql = "REPLACE INTO Port (port_domain,port_ip,port_port,port_server, port_http_status, port_time, port_target, port_new,port_user) VALUES('{}', '{}', '{}', '{}', {}, '{}', '{}',{},'{}');".format(
            host,
            result['ip'],
            str(result['port']),
            result['server'],
            False,
            time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())), 
            target_id,
            0,
            str(current_user)
        )
        cursor.execute(sql)
        conn.commit()
    return