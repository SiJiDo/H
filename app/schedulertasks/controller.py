from apscheduler.schedulers.background import BackgroundScheduler
from os import system
from multiprocessing import Process
from app.scan.conn import dbconn
from app.schedulertasks.emailsend import Sendemail
from app.schedulertasks.daliyscan import scan_daliy_vuln
from app.schedulertasks.schedulerscan import scheduler_scan
import time
import pytz

TZ = pytz.timezone("Asia/Shanghai")

def RunScheduler():
    scheduler = BackgroundScheduler(timezone=TZ)
    conn, cursor = dbconn()
    #获取发送邮件信息
    sql = "SELECT config_info,config_push_hour,config_email_username,config_email_password,config_email_server,config_email_get FROM Sysconfig"
    cursor.execute(sql)
    sysconfig_result = cursor.fetchone()

    #获取定时扫描的任务
    sql = "SELECT id,target_cron_id,target_user FROM Target WHERE target_cron = true AND target_pid = 0"
    cursor.execute(sql)
    tmp = cursor.fetchall()
    target_corn_results = []
    for i in tmp:
        dic = {}
        dic['id'] = i[0]
        dic['target_cron_id'] = i[1]
        dic['target_user'] = i[2]
        sql = "SELECT scancron_month, scancron_week, scancron_day, scancron_hour, scancron_min FROM Scancron WHERE id = %s"
        cursor.execute(sql,(dic['target_cron_id']))
        scheduler_config = cursor.fetchone()
        dic['scancron_month'] = scheduler_config[0]
        dic['scancron_week'] = scheduler_config[1]
        dic['scancron_day'] = scheduler_config[2]
        dic['scancron_hour'] = scheduler_config[3]
        dic['scancron_min'] = scheduler_config[4]
        target_corn_results.append(dic)

    cursor.close()
    conn.close()

    #邮件定时
    scheduler.add_job(Sendemail, 'cron', args=[True, ], month='*', day='*', day_of_week='*' ,hour=sysconfig_result[1], minute='0')
    #漏洞扫描定时
    scheduler.add_job(scan_daliy_vuln, 'cron', args=[ ], month='*', day='*', day_of_week='*' ,hour='0', minute='0')
    #定时扫描定时
    for target_cron_result in target_corn_results:
        scheduler.add_job(scheduler_scan,'cron', args=[target_cron_result['id'],target_cron_result['target_user'], ], month=dic['scancron_month'], day=dic['scancron_day'], day_of_week=dic['scancron_week'] ,hour=dic['scancron_hour'], minute=dic['scancron_min'])
    
    scheduler.start()

    while(1):
        time.sleep(10000)
            
    return

def restart_scheduler():
    conn, cursor = dbconn()
    sql = "SELECT * FROM Cronjob"
    cursor.execute(sql)
    result = cursor.fetchone()[1]
    if result != 0:
        system("kill " + result)
        p = Process(target=RunScheduler,args=())
        p.start()
        sql = "UPDATE Cronjob set cronjob_pid = %s"
        cursor.execute(sql,(str(p.pid)))
        conn.commit()
    return