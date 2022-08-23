from distutils.command.clean import clean
from celery import Celery
from app.home.target.models import Celerytask
from app.home.utils import *
import time 
import configparser
from app.scan.conn import dbconn
import queue
from threading import *

cfg = configparser.ConfigParser()
cfg.read('config.ini')

lock=Lock()

def scan_subdomain(scanmethod_query, target_id, current_user):
    #初始化数据库连接
    conn,cursor = dbconn()
    info = "target id:{} ---- 开始收集域名".format(target_id)
    sql = "INSERT INTO Runlog(log_info, log_time) VALUE('{}', '{}')".format(info, str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))))
    cursor.execute(sql)
    conn.commit()

    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)

    #查询该目标的主域
    sql = "SELECT * FROM Domain where domain_target = %s"
    cursor.execute(sql,(target_id))
    domain_query = cursor.fetchall()

    if(scanmethod_query[0] == True):
        tool_subfinder(task, domain_query, target_id, conn, cursor, current_user)
    if(scanmethod_query[1] == True):
        tool_amass(task, domain_query, target_id, conn, cursor, current_user)
    if(scanmethod_query[2] == True):
        tool_shuffledns(task, domain_query, target_id, conn, cursor, current_user)
    if(scanmethod_query[3] == True):
        sql = "SELECT * FROM Subdomain where subdomain_target = %s"
        cursor.execute(sql,(target_id,))
        domain_query = cursor.fetchall()
        tool_second(task, domain_query, target_id, conn, cursor, current_user)

    tool_domaininfo(task, target_id, conn, cursor)
    #关闭数据库句柄
    cursor.close()
    conn.close()
    return

#subfinder
def tool_subfinder(task, domain_query, target_id, conn, cursor, current_user):
    #开始扫描
    for domain_info in domain_query:
        #发送celery,subfinder扫描
        subfinder_scan = task.send_task('subfinder.run', args=(domain_info[1],), queue='subfinder')
        sql = "INSERT INTO Celerytask(celery_target, celery_id) VALUES(%s,%s)"
        cursor.execute(sql,(target_id, subfinder_scan.id,))
        conn.commit()

        while True:
            if subfinder_scan.successful():
                try:
                    save_result(target_id, subfinder_scan.result, conn, cursor, current_user)
                    break
                except Exception as e:
                    print(e)
                    break
                finally:
                    sql = "DELETE FROM Celerytask WHERE celery_id= %s"
                    cursor.execute(sql,(subfinder_scan.id,))
                    conn.commit()
    sql = "DELETE FROM Celerytask WHERE celery_target= %s"
    cursor.execute(sql,(target_id,))
    conn.commit()
    return

#amass
def tool_amass(task, domain_query, target_id, conn, cursor, current_user):

    for domain_info in domain_query:
        amass_scan = task.send_task('amass.run', args=(domain_info[1],), queue='amass')
        sql = "INSERT INTO Celerytask(celery_target, celery_id) VALUES(%s,%s)"
        cursor.execute(sql,(target_id, amass_scan.id,))
        conn.commit()
        while True:
            if amass_scan.successful():
                try:
                    save_result(target_id, amass_scan.result, conn, cursor, current_user)
                    break
                except Exception as e:
                    print(e)
                    break
    sql = "DELETE FROM Celerytask WHERE celery_target= %s"
    cursor.execute(sql,(target_id,))
    conn.commit()
    return


#shuffledns扫描
def tool_shuffledns(task, domain_query, target_id, conn, cursor, current_user):

    #爆破主域名
    config = False
    #初始化多线程
    thread_count = 10
    domain_queue = queue.Queue()
    #开始扫描
    for domain_info in domain_query:
        domain_queue.put(domain_info[1])

    # 使用多线程
    threads = []
    for i in range(0, thread_count):
        thread = Shufflednsscan(domain_queue, config, task, target_id, cursor, conn, current_user )
        thread.start()
        threads.append(thread)
    for j in threads:
        j.join()

    sql = "DELETE FROM Celerytask WHERE celery_target= %s"
    cursor.execute(sql,(target_id,))
    conn.commit()
    return

#shuffledns 二级域名扫描扫描
def tool_second(task, domain_query, target_id, conn, cursor, current_user):
    
    #爆破子域名的子域名
    config = True
    #初始化多线程
    thread_count = 10
    domain_queue = queue.Queue()
    #开始扫描
    for domain_info in domain_query:
        domain_queue.put(domain_info[1])

    # 使用多线程
    threads = []
    for i in range(0, thread_count):
        thread = Shufflednsscan(domain_queue, config, task, target_id, cursor, conn, current_user )
        thread.start()
        threads.append(thread)
    for j in threads:
        j.join()

    sql = "DELETE FROM Celerytask WHERE celery_target= %s"
    cursor.execute(sql,(target_id,))
    conn.commit()
    return

#domaininfo
def tool_domaininfo(task, target_id, conn, cursor):
    # 上限500个一组丢入查询
    sql = "SELECT subdomain_name FROM Subdomain WHERE subdomain_ip=%s AND subdomain_info=%s AND subdomain_target = %s LIMIT 500"
    ip_count = cursor.execute(sql,('nothing','nothing',target_id,))
    subdomain_result = cursor.fetchall()
    while(ip_count > 0):
        
        #转换为list
        sub_list = []
        for sub in subdomain_result:
            sub_list.append(sub[0])

        domaininfo_scan = task.send_task('domaininfo.run', args=(sub_list,), queue='domaininfo')
        while True:
            if domaininfo_scan.successful():
                try:
                    #print(domaininfo_scan.result)
                    save_result_domaininfo(target_id, domaininfo_scan.result, cursor, conn)
                except Exception as e:
                    print(e)
                finally:
                    break
        ip_count = cursor.execute(sql,('nothing','nothing',target_id,))
        subdomain_result = cursor.fetchall()

    sql = "DELETE FROM Subdomain where subdomain_ip='nothing' AND subdomain_info='nothing"
    cursor.execute(sql)
    conn.commit()
    return

#数据入库
def save_result(target_id, result, conn, cursor, current_user):
    result_info = result['result']
    result_tool = result['tool']
    for sub in result_info:
        #黑名单过滤
        if(black_list_query_scan(target_id, sub, '', cursor, conn)):
            continue
        #入库
        
        sql = "SELECT * FROM Subdomain where subdomain_name = %s AND subdomain_tool = %s AND subdomain_new=1"
        sql2 = "SELECT * FROM Subdomain where subdomain_name = %s AND subdomain_tool = %s AND subdomain_new=0"
        r = cursor.execute(sql2,(sub,result_tool,))
        tmptime = cursor.fetchone()
        
        if(cursor.execute(sql,(sub,result_tool,)) > 0):
            sql = "UPDATE Subdomain SET subdomain_ip='{}', subdomain_info='{}', subdomain_new={}  WHERE subdomain_name='{}'".format(
                'nothing', 
                'nothing', 
                1,
                sub,
            )
            result = cursor.execute(sql)
        elif(r >0 and str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) not in str(tmptime[7])):

            sql = "UPDATE Subdomain SET subdomain_ip='{}', subdomain_info='{}', subdomain_new={}  WHERE subdomain_name='{}'".format(
                'nothing', 
                'nothing', 
                1,
                sub,
            )
            result = cursor.execute(sql)

        else:
            sql = "REPLACE INTO Subdomain (subdomain_name,subdomain_ip,subdomain_info, subdomain_time, subdomain_target, subdomain_user, subdomain_tool, subdomain_new) VALUES('{}', '{}', '{}', '{}', '{}','{}','{}','{}')".format(
                sub,    #域名
                "nothing",  #ip地址
                "nothing",  #cname还是a记录
                time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())), #时间
                target_id,  #隶属的ip
                str(current_user), #扫描用户
                result_tool,    #工具
                0,
            )
            result = cursor.execute(sql)
        conn.commit()
    return 

def save_result_domaininfo(target_id, result, cursor, conn):
    result_info = result['result']
    for i in result_info:
        if('ips' in i and 'domain' in i):
            i['domain'] = i['domain'].strip()
            i['domain'].replace("'","\'")
            #排除黑名单和ip个数超过5个的站点(防止cdn)
            sql = "SELECT * FROM Subdomain where subdomain_ip = %s"
            ip_count = cursor.execute(sql,(','.join(i['ips'])))
            if(black_list_query_scan(target_id, '', ','.join(i['ips']),cursor,conn) #黑名单
                or
            ip_count > 5                                                         #ip个数大于5
            ):
                sql = "DELETE FROM Subdomain WHERE subdomain_name=%s"
                cursor.execute(sql,(i['domain'],))
                conn.commit()

            else:
                sql = "UPDATE Subdomain SET subdomain_ip='{}', subdomain_info='{}' WHERE subdomain_name='{}'".format(
                        ",".join(i['ips'][:3]), 
                        i['type'], 
                        i['domain'],
                    )
                cursor.execute(sql)
                conn.commit()
    return


class Shufflednsscan(Thread):
    def __init__(self, domain_query, config, task, target_id, cursor, conn, current_user):
        Thread.__init__(self)
        self.queue = domain_query
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
            domain_info = queue.get()
            #发送celery
            #shuffledns
            if(config == True):
                shuffledns_scan = task.send_task('shuffledns.run', args=(domain_info,'top100.txt',), queue='shuffledns')
            else:
                shuffledns_scan = task.send_task('shuffledns.run', args=(domain_info,), queue='shuffledns')
            sql = "INSERT INTO Celerytask(celery_target, celery_id) VALUES(%s,%s)"
            lock.acquire()
            cursor.execute(sql,(target_id, shuffledns_scan.id,))
            conn.commit()
            lock.release()
            while True:
                if shuffledns_scan.successful():
                    
                    lock.acquire()
                    save_result(target_id, shuffledns_scan.result, conn, cursor, current_user)
                    lock.release()
                    break
                        

                #print("[-]host unknow")

        return
