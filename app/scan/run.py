from app.home.target.models import Target
from app.scan.lib.Scansubdomain import scan_subdomain
from app.scan.lib.Scanport import scan_port
from app.scan.lib.Scanhttp import scan_http
from app.scan.lib.Scandir import scan_dir
from app.scan.lib.Scanvuln import scan_vuln
from app.home.vuln.models import Vuln
from app.home.http.models import Http
from time import sleep
from flask import request, redirect, url_for
from flask_login import current_user
from multiprocessing import Process
from app import db
import os
from app.scan.conn import dbconn
import time

#开始扫描
def startscan():
    id = request.args.get('id')
    current = str(current_user)
    p = Process(target=startscan_process,args=(id, current, ))
    p.start()
    db.session.query(Target).filter(Target.id == id).update({'target_pid':p.pid, 'target_status': 1})
    db.session.commit()

    return redirect(url_for('home_blueprint.targetinforoute',id=id,message="开始扫描, 扫描进程为----" + str(p.pid)))

#暂停扫描
def stopscan():
    id = request.args.get('id')
    pid = ""
    db.session.query(Target).filter(Target.id == id).update({'target_pid':0})
    db.session.query(Target).filter(Target.id == id).update({'target_status':0})
    db.session.commit()
    try:
        target = db.session.query(Target).filter(Target.id == id).first()
        pid = target.target_pid
        if(pid != 0):
            os.system("kill " + str(pid))
    except Exception as e:
        print(e)
        return redirect(url_for('home_blueprint.targetinforoute',id=id,message="内部错误"))
    
    return redirect(url_for('home_blueprint.targetinforoute',id=id,message="停止扫描, 扫描进程为----" + str(pid)))

#开始扫描
def webhook():
    vuln = request.json
    if "web_statistic" in vuln['type']:
        return "ok"

    target_name = vuln["data"]["detail"]["addr"].split("://")[1].split("/")[0]
    print("target_name : " + target_name )
    if(":" not in target_name):
        if(vuln["data"]["detail"]["addr"].split("://")[0] == 'https'):
            target_name = target_name + ":443"
        else:
            target_name = target_name + ":80"
    

    result = db.session.query(Http).filter(Http.http_name == target_name).first()
    v = Vuln()
    v.vuln_mainkey = str(vuln["data"]["detail"]["addr"] + vuln["data"]["plugin"])[:100]
    v.vuln_info = vuln["data"]["plugin"]
    v.vuln_poc = vuln["data"]["detail"]["addr"]
    v.vuln_level = "xray"
    v.vuln_tool = "xray"
    v.vuln_time = str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))
    v.vuln_new = 0
    
    if(result):
        v.vuln_user = result.http_user
        v.vuln_http = result.id
        v.vuln_target = result.http_target
        v.vuln_name = result.http_schema + "://" + result.http_name
    else:
        v.vuln_user = None
        v.vuln_http = None
        v.vuln_target = None
        v.vuln_name = vuln["data"]["detail"]["addr"].split("://")[0] + "://" + vuln["data"]["detail"]["addr"].split("://")[1].split("/")[0]

    count = db.session.query(Vuln).filter(Vuln.vuln_mainkey == v.vuln_mainkey).count()
    if(count > 0):
        db.session.query(Vuln).filter(Vuln.vuln_mainkey == v.vuln_mainkey).update({Vuln.vuln_new:1})
    else:
        print("入库:" + v.vuln_poc)
        db.session.add(v)
    db.session.commit()

    return 'ok'


#开始扫描，注意是子进程需要起新的句柄进行数据库连接
def startscan_process(id, current_user):
    #建立连接
    sleep(3)
    conn, cursor = dbconn()
    info = "target id:{} ---- 进入扫描等待".format(id)
    sql = "INSERT INTO Runlog(log_info, log_time) VALUE('{}', '{}')".format(info, str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))))
    cursor.execute(sql)
    conn.commit()

    #判断当前扫描任务是否达到上限,达到上限就等待
    sql = "SELECT config_count FROM Sysconfig"
    cursor.execute(sql)
    max_count = cursor.fetchone()[0]
    sql = "SELECT * FROM Target where target_status > 1 AND target_status < 6"
    scan_count = cursor.execute(sql)
    while(scan_count >= max_count):
        sleep(60)

    #有机会扫描了，将其标志位设置为2
    sql = "SELECT * FROM Target where (target_status = 1 or target_status = 7) and id = %s"
    target_status = cursor.execute(sql,(id))
    if(target_status == 0):
        print("项目正在运行")
        return

    
    sql = '''SELECT scanmethod_subfinder,
                scanmethod_amass,
                scanmethod_shuffledns,
                scanmethod_second,
                scanmethod_port,
                scanmethod_port_portlist,
                scanmethod_port_dfportlist,
                scanmethod_httpx,
                scanmethod_ehole,
                scanmethod_screenshot,
                scanmethod_jsfinder,
                scanmethod_dirb,
                scanmethod_dirb_wordlist,
                scanmethod_xray,
                scanmethod_nuclei,
                scanmethod_nuclei_my 
                FROM Scanmethod,Target where Scanmethod.id = Target.target_method and Target.id = %s'''             
    cursor.execute(sql,(id))
    scanmethod_query = cursor.fetchone()

    sql = "UPDATE Target SET target_status=%s WHERE id=%s"
    cursor.execute(sql,(2,id))
    conn.commit()

    #关闭连接(长时间连接会超时)
    cursor.close()
    conn.close()

    #开始收集域名 --- 2
    scan_subdomain(scanmethod_query, id, current_user)
    #开始收集端口 --- 3
    changestatus(3,id)
    scan_port(scanmethod_query, id, current_user)
    #开始收集站点信息 --- 4
    changestatus(4,id)
    scan_http(scanmethod_query, id, current_user)
    #开始收集目录 --- 5
    changestatus(5,id)
    scan_dir(scanmethod_query, id, current_user)
    #开始扫描漏洞 --- 6
    changestatus(6,id)
    scan_vuln(scanmethod_query, id, current_user)
    #结束 --- 7
    scan_over(id)
    sleep(5)

    return

def scan_over(id):
    #建立数据库连接
    conn, cursor = dbconn()

    #关闭该项目-设置pid为0， 设置项目状态为完成(7)
    sql = "SELECT target_pid from Target WHERE id=%s"
    cursor.execute(sql,(id))
    pid = cursor.fetchone()[0]
    try:
        os.system("kill " + str(pid))
    except:
        pass

    sql = "UPDATE Target SET target_pid=%s, target_status=%s WHERE id=%s"
    cursor.execute(sql,(0,7,id))
    conn.commit()

    info = "target id:{} ---- 扫描结束".format(id)
    sql = "INSERT INTO Runlog(log_info, log_time) VALUE('{}', '{}')".format(info, str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))))
    cursor.execute(sql)
    conn.commit()

    #关闭连接
    cursor.close()
    conn.close()
    return

def changestatus(setid,id):

    #建立数据库连接
    conn, cursor = dbconn()

    #关闭该项目-设置pid为0， 设置项目状态为完成(6)
    sql = "UPDATE Target SET target_status=%s WHERE id=%s"
    cursor.execute(sql,(setid,id))
    conn.commit()

    #关闭连接
    cursor.close()
    conn.close()
    return
