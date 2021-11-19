from flask import render_template
from flask.globals import request
import os
import time
from subprocess import Popen

from app.plugins.hostcrack.forms import HostcrackForm
from app.plugins.hostcrack.models import plugins_Hostcrack
from app.home import utils
from app.home.target.function import *
from app.scan.conn import dbconn
from multiprocessing import Process
import math

FILEPATH = os.path.split(os.path.realpath(__file__))[0]

def hostcrack(DynamicModel = plugins_Hostcrack, DynamicFrom = HostcrackForm):
    page = int(request.args.get('page')) if request.args.get('page') else 1
    DynamicFrom = HostcrackForm()
    if ( request.method == 'POST'):
        #自动生成内网样子的host
        if(request.args.get("action") == 'create'):
            result = createdomain(request.form['maindomain'])
            host = {}
            host['hostcrack_ip'] = ''
            host['hostcrack_domain'] = '\n'.join(result)
            utils.dict_to_form(host, DynamicFrom)
            
        #碰撞
        elif(request.args.get("action") == 'crack'):
            nowtime = str(time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())))
            
            p = Process(target=crack,args=(request.form['hostcrack_ip'], request.form['hostcrack_domain'],nowtime, ))
            p.start()
            conn, cursor = dbconn()
            sql = "INSERT INTO plugins_Hostcrack(hostcrack_domain, hostcrack_ip, hostcrack_pid, hostcrack_time) VALUE(%s,%s,%s,%s)"
            cursor.execute(sql,(request.form['hostcrack_domain'],request.form['hostcrack_ip'],str(p.pid), nowtime))
            conn.commit()
            cursor.close()
            conn.close()
    if ( request.method == 'GET'):
        id = request.args.get("id")
        if(id):
            if(request.args.get("action") == 'delete'):
                db.session.query(DynamicModel).filter(DynamicModel.id == id).delete()
                db.session.commit()
            else:
                query = db.session.query(DynamicModel).filter(DynamicModel.id == id).first()
                nowhostcarck = utils.queryToDict(query)
                utils.dict_to_form(nowhostcarck, DynamicFrom)
            # print(query.hostcrack_time)
    
    query = db.session.query(DynamicModel).order_by(DynamicModel.id.desc()).paginate(page, 5)
    total_count = db.session.query(DynamicModel).count()
    result = []
    for q in query.items:        
        result.append(queryToDict(q))

    for r in result:
        r["hostcrack_time"] = q.hostcrack_time
        r["hostcrack_domain"] = ",".join(q.hostcrack_domain[0:30].split("\r\n")) + "....."
        r["hostcrack_ip"] = ",".join(q.hostcrack_ip[0:30].split("\r\n")) + "....."
        r["hostcrack_result"] = q.hostcrack_result[0:30] + "....."
        r["status"] = "运行结束" if q.hostcrack_pid == '0' else "正在运行"
    
    content = {'result': result, 'total_page': math.ceil(total_count / 5), 'page': page,}

    return render_template('hostcrack.html', segment='hostcrack', form = DynamicFrom, content = content, )

#自动生成内网host
def createdomain(maindomain):
    maindomain_list = maindomain.split('.')
    intralist = open(FILEPATH + "/tools/intralist.txt", "r") 
    sublist = open(FILEPATH + "/tools/sublist.txt", "r")
    tmpdomain = []
    tmpsub = []
    result = []

    for sl in sublist.readlines():
        tmpsub.append(sl)

    for il in intralist.readlines():
        il = il.strip()
        tmpdomain.append(il + '.' + '.'.join(maindomain_list))

    for tmp in tmpdomain:
        for sl in tmpsub:
            sl = sl.strip()
            result.append(sl + '.' + tmp)
    return result

#碰撞(子进程运行，不然会卡死)
def crack(hostcrack_ip, hostcrack_domain, nowtime):
    ip_file = FILEPATH + '/tools/' + 'ip_{}.txt'.format(str(time.time()))
    domain_file = FILEPATH + '/tools/' + 'domain_{}.txt'.format(str(time.time()))
    output_file = FILEPATH + '/tools/' + 'output_{}.txt'.format(str(time.time()))
    f_ip_file = open(ip_file,'a')
    f_domain_file = open(domain_file,'a')
    hostcrack_ip_target = []

    for ip in hostcrack_ip.split('\r\n'):
        if("-" in ip):
            try:
                hostcrack_ip_target += getip1(ip)
            except Exception as e:
                print(e)
        elif("/" in ip):
            try:
                hostcrack_ip_target = hostcrack_ip_target + getip2(ip)
            except Exception as e:
                print(e)
        else:
            hostcrack_ip_target.append(ip)
        
    for i in hostcrack_ip_target:
        f_ip_file.write(str(i).strip() + '\r\n')
    
    for i in hostcrack_domain.split('\r\n'):
        f_domain_file.write(i + '\r\n')
        
    f_ip_file.close()
    f_domain_file.close()
    
    command = '{}hostscan -T 50 -I {} -D {} -O {}'.format(FILEPATH + '/tools/', ip_file, domain_file, output_file)
    cmd = Popen(command, shell=True)
    while 1:
        ret = Popen.poll(cmd)
        if ret == 0:
            break
    result = ""
    try:
        f_output_file = open(output_file, 'r')
        for line in f_output_file.readlines():
            line = line.strip()
            result = result + line + '\r\n'
    except:
        result = ""

    try:
        pass
        os.system("rm -rf {}".format(ip_file))
        os.system("rm -rf {}".format(domain_file))
        os.system("rm -rf {}".format(output_file))
    except:
        pass

    conn, cursor = dbconn()

    sql = "UPDATE plugins_Hostcrack SET hostcrack_result=%s WHERE hostcrack_time=%s"
    cursor.execute(sql,(result,nowtime))
    conn.commit()

    sql = "UPDATE plugins_Hostcrack SET hostcrack_pid='0' WHERE hostcrack_time=%s"
    cursor.execute(sql,(nowtime))
    conn.commit()
    cursor.close()
    conn.close()
