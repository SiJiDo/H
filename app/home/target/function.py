from app.home.target.models import Blacklist
from app.home.domain.models import Domain
from app.home.subdomain.models import Subdomain
from app.home.port.models import Port
from app.home.http.models import Http
from app.home.utils import *
import time
from app import db
import IPy
import re
import xlwt

#保存域名
def savedomain(domain_name, id, current_user):
    domain_list = domain_name.split('\r\n')
    for i in domain_list:
        if(Domain.query.filter(Domain.domain_name == i).count() > 0):
            continue
        domain = Domain()
        domain.domain_name = i
        domain.domain_target = id
        domain.domain_subdomain_status = False
        domain.domain_user = str(current_user)
        domain.domain_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
        db.session.add(domain)
        db.session.commit()
    return 

#保存黑名单
def saveblacklist(black_name, id):
    black_list = black_name.split('\r\n')
    for i in black_list:
        if(Blacklist.query.filter(Blacklist.black_name == i).count() > 0):
            continue
        blacklist = Blacklist()
        blacklist.black_name = i
        blacklist.black_target = id
        blacklist.black_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
        db.session.add(blacklist)
        db.session.commit()
        blacklist_remove(i,id)
    return

#保存精准域名或ip信息
def savesubdomain(subdomain_name, id, current_user):
    subdomain_list = subdomain_name.split('\r\n')
    for i in subdomain_list:
        isdomain = re.search( r'[a-zA-Z]', i)
        if(isdomain):
            try:
                subdomain = Subdomain()
                subdomain.subdomain_name = i
                subdomain.subdomain_target = id
                subdomain.subdomain_http_status = False
                subdomain.subdomain_port_status = False
                subdomain.subdomain_tool = "Add by user"
                subdomain.subdomain_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
                subdomain.subdomain_user = str(current_user)
                subdomain.subdomain_ip = "nothing"
                subdomain.subdomain_info = "nothing"
                subdomain.subdomain_new = 0
                db.session.add(subdomain)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
        else:
            saveip(i,id,current_user)

    return

#保存ip
def saveip(ip_name, id, current_user):
    subdomain_list = ip_name.split('\r\n')
    subdomain_last_list = []
    for i in subdomain_list:
        if("-" in i):
            try:
                subdomain_last_list += getip1(i)
            except Exception as e:
                print(e)
        elif("/" in i):
            try:
                subdomain_last_list = subdomain_last_list + getip2(i)
            except Exception as e:
                print(e)
        else:
            subdomain_last_list.append(i)
    for i in subdomain_last_list:
        i = str(i).strip()
        if(not i):
            continue
        #黑名单过滤
        if(black_list_query(id, '', i)):
            continue
        i = i.replace("'","\'")
        try:
            subdomain = Subdomain()
            subdomain.subdomain_name = i
            subdomain.subdomain_target = id
            subdomain.subdomain_http_status = False
            subdomain.subdomain_port_status = False
            subdomain.subdomain_tool = "Add by user"
            subdomain.subdomain_time = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
            subdomain.subdomain_user = str(current_user)
            subdomain.subdomain_ip = i
            subdomain.subdomain_info = "UNKNOW"
            subdomain.subdomain_new = 0
            db.session.add(subdomain)
            db.session.commit()
        except Exception as e:
                print(e)
                db.session.rollback()
    return

#删除属于添加黑名单的信息(有待完善)
def blacklist_remove(black, target_id):
    if("domain:" in black):
        b = black.split("domain:")[1]
        try:
            result = Subdomain.query.filter(Subdomain.subdomain_name.like("%{}%".format(b)), Subdomain.subdomain_target == target_id).all()
            [db.session.delete(r) for r in result]
            result = Port.query.filter(Port.port_domain.like("%{}%".format(b)), Port.port_target == target_id).all()
            [db.session.delete(r) for r in result]
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    if("ip:" in black):
        b = black.split("ip:")[1]
        try:
            result = Subdomain.query.filter(Subdomain.subdomain_ip.like("%{}%".format(b)), Subdomain.subdomain_target == target_id).all()
            [db.session.delete(r) for r in result]
            result = Port.query.filter(Port.port_ip.like("%{}%".format(b)), Port.port_target == target_id).all()
            [db.session.delete(r) for r in result]
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    if("title:" in black):
        b = black.split("title:")[1]
        try:
            result = Http.query.filter(Http.http_title.like("%{}%".format(b)), Http.http_target == target_id).all()
            [db.session.delete(r) for r in result]
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()



#获取/24带子网掩码的ip
def getip2(ips):
    ip = IPy.IP(ips)
    return list(ip)

#获取带-的ip列表
def getip1(ip):
    last = ""
    test = ip.split('.')
    zone = []
    result = []
    count = 0
    for i in test:
        if("-" not in i):
            last = last + i + '.'
        if("-" in i):
            last = last + 'temp' + str(count) + '.'
            zone.append(int(i.split("-")[0]))
            zone.append(int(i.split("-")[1]))
            count = count + 1

    last = last[:-1]

    if len(zone) == 2: 
        for i in range(zone[0], zone[1] + 1):
            result.append(last.replace("temp0", str(i)))

    if len(zone) == 4:
        for i in range(zone[0], zone[1] + 1):
            for j in range(zone[2], zone[3] + 1):
                temp = last.replace("temp0", str(i))
                temp = temp.replace("temp1", str(j))
                result.append(temp)

    if len(zone) == 6:
        for i in range(zone[0], zone[1] + 1):
            for j in range(zone[2], zone[3] + 1):
                for k in range(zone[4], zone[5] + 1):
                    temp = last.replace("temp0", str(i))
                    temp = temp.replace("temp1", str(j))
                    temp = temp.replace("temp2", str(k))
                    result.append(temp)

    if len(zone) == 8:
        for i in range(zone[0], zone[1] + 1):
            for j in range(zone[2], zone[3] + 1):
                for k in range(zone[4], zone[5] + 1):
                    for v in range(zone[6], zone[7] + 1):
                        temp = last.replace("temp0", str(i))
                        temp = temp.replace("temp1", str(j))
                        temp = temp.replace("temp2", str(k))
                        temp = temp.replace("temp3", str(v))
                        result.append(temp)
    return result