from celery import Celery
from app.home.utils import *
from app.home.utils import *
import time 
import configparser
from threading import *
from app.scan.conn import dbconn

cfg = configparser.ConfigParser()
cfg.read('config.ini')

def scan_http(scanmethod_query, target_id, current_user):

    #初始化数据库连接
    conn,cursor = dbconn()
    info = "target id:{} ---- 开始收集站点".format(target_id)
    sql = "INSERT INTO Runlog(log_info, log_time) VALUE('{}', '{}')".format(info, str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))))
    cursor.execute(sql)
    conn.commit()
    task = Celery(broker=cfg.get("CELERY_CONFIG", "CELERY_BROKER_URL"), backend=cfg.get("CELERY_CONFIG", "CELERY_RESULT_BACKEND"))
    task.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)

    #查询该目标的未扫描的域名
    sql = "SELECT * FROM Subdomain WHERE subdomain_target=%s "
    cursor.execute(sql,(target_id,))
    subdomain_query = cursor.fetchall()
    sql = "SELECT * FROM Port WHERE port_target=%s"
    cursor.execute(sql,(target_id,))
    port_query = cursor.fetchall()
    #将结果保存为list
    subdomain_list = []
    for subdomain_info in subdomain_query:
        subdomain_list.append(subdomain_info[1])
    #根据ip获取http信息，排除80,443端口
    for port_info in port_query:
        if(port_info[3] == '443' or port_info[3] == '80'):
            continue
        subdomain_list.append(port_info[1] + ':' + port_info[3])
    #获取http信息
    if(scanmethod_query[7] == True):
        tool_httpx(task, subdomain_list, target_id, conn, cursor, current_user)
    #截图     
    if(scanmethod_query[8] == True):
        tool_screenshot(task, target_id, conn, cursor)
    #获取指纹
    if(scanmethod_query[9] == True):
        tool_ehole(task, target_id, conn, cursor)

    cursor.close()
    conn.close()
    return


#httpx
def tool_httpx(task, subdomain_list, target_id, conn, cursor, current_user):
    # 上限100个一组丢入查询
    sub_list = subdomain_list[0:100] if len(subdomain_list) > 100 else subdomain_list
    
    while(len(subdomain_list)):
        httpx_scan = task.send_task('httpx.run', args=(sub_list,), queue='httpx')
        while True:
            if httpx_scan.successful():
                try:
                    save_result(target_id, httpx_scan.result['result'], cursor, conn, current_user)
                except Exception as e:
                    print(e)
                finally:
                    break


        subdomain_list = subdomain_list[100:]
        sub_list = subdomain_list[0:100] if len(subdomain_list) > 100 else subdomain_list

    return

#截图功能
def tool_screenshot(task, target_id, conn, cursor):
    #截图，注意数据太多会失败
    sql = "SELECT * FROM Http WHERE http_target=%s AND http_screen=%s AND http_status!=%s AND http_status!=%s LIMIT 100"
    screen_count = cursor.execute(sql,(target_id,'No','302','301'))
    http_query_all = cursor.fetchall()
    while(screen_count > 0):
        http_list = []
        for http_info in http_query_all:
            http_list.append(http_info[1] + "://" + http_info[2])
            
        screenshot_scan = task.send_task('screenshot.run', args=(http_list,), queue='screenshot')
        while True:
            if screenshot_scan.successful():
                try:
                    save_result_screenshot(screenshot_scan.result['result'], cursor, conn)
                except Exception as e:
                    print(e)
                finally:
                    break
        screen_count = cursor.execute(sql,(target_id,'No','302','301'))
        http_query_all = cursor.fetchall()
    return

#ehole指纹获取
def tool_ehole(task, target_id, conn, cursor):
    sql = "SELECT * FROM Http WHERE http_target=%s AND http_finger=%s LIMIT 100"
    finger_count = cursor.execute(sql,(target_id,'No',))
    http_query_all = cursor.fetchall()
    while(finger_count > 0):
        http_list = []
        for http_info in http_query_all:
            http_list.append(http_info[1] + "://" + http_info[2])
            sql = "UPDATE Http set http_finger='' WHERE http_target=%s AND http_name=%s "
            cursor.execute(sql,(target_id, http_info[2]))
            conn.commit()
        
        finger_scan = task.send_task('ehole.run', args=(http_list,), queue='ehole')
        while True:
            if finger_scan.successful():
                try:
                    save_result_finger(finger_scan.result['result'], cursor, conn)
                except Exception as e:
                    print(e)
                finally:
                    break
        finger_count = cursor.execute(sql,(target_id,'No',))
        http_query_all = cursor.fetchall()

    return

#子域名的http扫描
def save_result(target_id, http_result, cursor, conn, current_user): 
    for result in http_result:
        #title黑名单过滤
        if(black_list_title_query(target_id, result['title'], cursor, conn)):
            continue
        if('\'' in result['title']):
            result['title'] = result['title'].replace("\'","\\\'")
        #入库
        print("开始http入库:" + result['url'])
        sql = "SELECT * FROM Http WHERE http_name=%s"
        count_result = cursor.execute(sql,(result['url'].split("://")[1],))
        if(count_result == 0):
            sql = "REPLACE INTO Http (http_schema,http_name,http_title,http_status, http_length, http_screen, http_finger, http_time, http_target, http_see, http_new, http_user ) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}');".format(
                result['url'].split("://")[0],
                result['url'].split("://")[1],
                result['title'],
                result['status-code'],
                result['content-length'],
                "No",
                "No",
                time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())), 
                target_id,
                0,
                0,
                str(current_user),
            )
            cursor.execute(sql)
            conn.commit()
        #存在判断是否有更新
        else:
            sql = "SELECT * FROM Http WHERE http_name=%s AND http_title=%s AND http_status=%s AND http_length=%s"
            count = cursor.execute(sql,(result['url'].split("://")[1],result['title'],result['status-code'],result['content-length'],))
            #没更新
            if(count == 1):
                sql = "UPDATE Http set  http_new=%s WHERE http_name=%s"
                cursor.execute(sql,(2,result['url'].split("://")[1]))
                conn.commit()

            #有更新
            else:
                sql = "UPDATE Http set  http_title=%s,http_status=%s,http_length=%s,http_screen=%s,http_finger=%s,http_time=%s, http_target=%s, http_see=%s, http_new=%s, http_user=%s WHERE http_name=%s"
                cursor.execute(sql,(result['title'],
                                    result['status-code'],
                                    result['content-length'],
                                    "No",
                                    "No",
                                    time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())),
                                    target_id,
                                    0,
                                    1, 
                                    str(current_user),
                                    result['url'].split("://")[1],
                                    )
                                )
                conn.commit()

    return

#截图
def save_result_screenshot(http_result, cursor, conn):  
    for result in http_result:
        print("开始存储截图:" + result['http'])
        print(result)
        try:
            sql='UPDATE Http SET http_screen=%s WHERE http_name=%s'
            result = cursor.execute(sql,(result['screen_base64'],result['http'].split("://")[1])) 
            conn.commit()
        except Exception as e:
            print(e)
    return

#保存指纹
def save_result_finger(http_result, cursor, conn):  
    for result in http_result:
        print("开始存储指纹:" + result['http_name'])
        print(result)
        try:
            sql='UPDATE Http SET http_finger=%s WHERE http_name=%s'
            result = cursor.execute(sql,(result['http_finger'],result['http_name'].split("://")[1])) 
            conn.commit()
        except Exception as e:
            print(e)
    return