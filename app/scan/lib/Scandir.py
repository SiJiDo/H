from celery import Celery
from app.home.utils import *
import time 
import configparser
from app.scan.conn import dbconn

cfg = configparser.ConfigParser()
cfg.read('config.ini')

def scan_dir(scanmethod_query, target_id, current_user):
    #初始化数据库连接
    conn,cursor = dbconn()
    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)

    #查询该目标的未扫描的域名
    sql = "SELECT * from Http WHERE http_target=%s"
    cursor.execute(sql,(target_id,))
    http_query = cursor.fetchall()

    if(scanmethod_query[10] == True):
        tool_jsfinder(task, http_query, target_id, conn, cursor, current_user)
    if(scanmethod_query[11] == True):
        #13是字典
        wordlist = scanmethod_query[12]
        tool_fileleak(task, http_query, wordlist, target_id, conn, cursor, current_user)

    #关闭数据库句柄
    cursor.close()
    conn.close()
    return 

def tool_jsfinder(task, http_query, target_id, conn, cursor, current_user):
    #开始扫描
    for target in http_query:
        url = target[1] + '://' + target[2]
        dir_scan = task.send_task('jsfinder.run', args=(url,), queue='jsfinder')
        while True:
            if dir_scan.successful():
                try:
                    save_result(target, target_id, dir_scan.result, cursor, conn, current_user)
                    break
                except Exception as e:
                    print(e)
                    break
    return

def tool_fileleak(task, http_query, wordlist, target_id, conn, cursor, current_user):
    #开始扫描
    for target in http_query:
        url = target[1] + '://' + target[2]
        dir_scan = task.send_task('fileleak.run', args=(url,wordlist,), queue='fileleak')
        while True:
            if dir_scan.successful():
                try:
                    save_result(target, target_id, dir_scan.result, cursor, conn, current_user)
                    break
                except Exception as e:
                    print(e)
                    break
    return

#保存
def save_result(target, target_id, result, cursor, conn, current_user): 
    tool = result['tool']
    result = result['result']
    for result in result:
        #过滤掉302
        if(result['status-code'] == '302' or result['status-code'] == '301'):
            continue
        #去掉根目录
        if(result['path'] == '' or result['path'] == '/'):
            continue

        #去掉可能相同页面
        sql = "SELECT * from Dirb WHERE dir_http=%s AND dir_length=%s"
        if(cursor.execute(sql,(target[0], result['content-length']))):
            #如果资产存在则标记已扫描
            print("判断过滤:" + result['host'] + result['path'])
            sql = "SELECT * from Dirb WHERE dir_base=%s"
            if(cursor.execute(sql,(result['host'] + result['path']))):
                sql = "UPDATE Dirb set dir_new=1 WHERE dir_base=%s"
                cursor.execute(sql,(result['host'] + result['path']))
                conn.commit()
    
        else:
            #入库
            print("dir入库:" + result['host'] + result['path'])
            try:
                sql = "REPLACE INTO Dirb (dir_base,dir_path,dir_length,dir_status, dir_title, dir_http, dir_time, dir_target, dir_tool, dir_user, dir_new) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {});".format(
                    result['host'] + result['path'],
                    result['path'],
                    result['content-length'],
                    result['status-code'],
                    result['title'],
                    target[0],
                    time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())), 
                    target_id,
                    tool,
                    str(current_user),
                    0,
                )
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(e)       
    