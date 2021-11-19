# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from app.scan.conn import dbconn
import time

def Sendemail(isdaliy=True, tool="", url="", info="", poc="", level="",scantime="" ):
    conn, cursor = dbconn()
    sql = "SELECT config_info,config_push_hour,config_email_username,config_email_password,config_email_server,config_email_get FROM Sysconfig"
    cursor.execute(sql)
    sysconfig_result = cursor.fetchone()
    receivers = sysconfig_result[5].split('\r\n')

    smtp_server = str(sysconfig_result[4])
    smtp_user = str(sysconfig_result[2])
    smtp_password = str(sysconfig_result[3])
    print("smtp_server=" + smtp_server)
    print("smtp_user=" + smtp_user)
    print("smtp_password=" + smtp_password)
    print(receivers)
    if(isdaliy==True):
        mail_msg = """
        <p>通知 - 资产情况</p>
        <p>资产详细如下</p>
        """
        sql = "SELECT target_name,id FROM Target"
        cursor.execute(sql)
        target_results = cursor.fetchall()

        for target_result in target_results:

            sql = "SELECT * FROM Subdomain WHERE subdomain_target=%s"
            subdomain_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Subdomain WHERE subdomain_target=%s AND subdomain_new=0"
            new_subdomain_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Subdomain WHERE subdomain_target='{}' AND subdomain_time like '%{}%'".format(target_result[1], time.strftime('%Y-%m-%d', time.localtime(time.time())))
            today_subdomain_count = str(cursor.execute(sql))

            sql = "SELECT * FROM Port WHERE port_target=%s"
            port_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Port WHERE port_target=%s AND port_new=0"
            new_port_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Port WHERE port_target='{}' AND port_time like '%{}%'".format(target_result[1], time.strftime('%Y-%m-%d', time.localtime(time.time())))
            today_port_count = str(cursor.execute(sql))

            sql = "SELECT * FROM Http WHERE http_target=%s"
            http_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Http WHERE http_target=%s AND http_new=0"
            new_http_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Http WHERE http_target='{}' AND http_time like '%{}%'".format(target_result[1], time.strftime('%Y-%m-%d', time.localtime(time.time())))
            today_http_count = str(cursor.execute(sql))

            sql = "SELECT * FROM Dirb WHERE dir_target=%s"
            dir_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Dirb WHERE dir_target=%s AND dir_new=0"
            new_dir_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Dirb WHERE dir_target='{}' AND dir_time like '%{}%'".format(target_result[1], time.strftime('%Y-%m-%d', time.localtime(time.time())))
            today_dir_count = str(cursor.execute(sql))

            sql = "SELECT * FROM Vuln WHERE vuln_target=%s"
            vuln_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Vuln WHERE vuln_target=%s AND vuln_new=0"
            new_vuln_count = str(cursor.execute(sql,(target_result[1])))
            sql = "SELECT * FROM Vuln WHERE vuln_target='{}' AND vuln_time like '%{}%'".format(target_result[1], time.strftime('%Y-%m-%d', time.localtime(time.time())))
            today_vuln_count = str(cursor.execute(sql))


            mail_msg = mail_msg + """
            <hr/>
            <p>{}</p>
            <table border="1" style="text-align:center;"><tr><th>子域名数(今日新增)(新增)</th><th>端口数(今日新增)(新增)</th><th>站点数(今日新增)(新增)</th><th>路径数(今日新增)(新增)</th><th>漏洞数(今日新增)(新增)</th></tr>
            <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr></table>
            """.format(target_result[0],
            subdomain_count + '(' + today_subdomain_count + ')' + '(' + new_subdomain_count + ')',
            port_count + '(' + today_port_count + ')' + '(' + new_port_count + ')',
            http_count + '(' + today_http_count + ')' + '(' + new_http_count + ')',
            dir_count + '(' + today_dir_count + ')' + '(' + new_dir_count + ')',
            vuln_count + '(' + today_vuln_count + ')' + '(' + new_vuln_count + ')',
            )
        
    else:
        mail_msg = """
        <p>通知 - 漏洞通知！！！</p>
        <p>{} 发现新漏洞:</p>
        <table border="1"><tr><th>漏洞站点</th><th>信息</th><th>poc</th><th>危害</th><th>发现时间</th></tr>
        <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr></table>
        """.format(tool,
                url,
                info,
                poc,
                level,
                scantime,
                    )

    message = MIMEText(mail_msg, 'html', 'utf-8')
    subject = 'H资产收集器通知'
    message['Subject'] = Header(subject, 'utf-8')

    cursor.close()
    conn.close()

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(smtp_server, 25)    # 25 为 SMTP 端口号
        smtpObj.login(smtp_user,smtp_password)
        smtpObj.sendmail(smtp_user, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
        return
     
if __name__ == '__main__':
    Sendemail()