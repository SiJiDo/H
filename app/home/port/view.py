from app.home.port.models import Port
from app.home.target.models import *
from app.home.utils import *
from flask import render_template, request
from app import db
from flask_login import current_user
import math

#target目录总览
def port(DynamicModel = Port):
    # 接收参数
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else 10
    query = ""
    search = ""
    total_count = ""

    #查询
    search = request.args.get('search')
    if search != 'None' and search and '=' in search:
        target = ""
        port_domain = ""
        port_ip = ""
        port_port = ""
        port_server = ""
        user = ""
        new = ""
        start_time = "2021-01-01 00:00:00"
        end_time = "2099-01-01 00:00:00"
        info = search.split("&&")
        for i in info:
            if('target' in i):
                target = i.split("=")[1]
            if('start_time' in i):
                start_time = i.split("=")[1]
            if('end_time' in i):
                end_time = i.split("=")[1]
            if('subdomain' in i):
                port_domain = i.split("=")[1]
            if('ip' in i):
                port_ip = i.split("=")[1]
            if('port' in i):
                port_port = i.split("=")[1]
            if('server' in i):
                port_server = i.split("=")[1]
            if('user' in i):
                user = i.split("=")[1]
            if('new' in i):
                new = 0 if i.split("=")[1] == 'true' else 1

        search = search.replace("&&", "%26%26")
        if(is_admin()):
            query = db.session.query(
                    DynamicModel.port_domain, 
                    DynamicModel.port_ip, 
                    DynamicModel.port_port,
                    DynamicModel.port_server,
                    DynamicModel.port_time,
                    DynamicModel.port_user,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.port_domain.like("%{}%".format(port_domain)),
                    DynamicModel.port_ip.like("%{}%".format(port_ip)),
                    DynamicModel.port_port.like("%{}%".format(port_port)),
                    DynamicModel.port_server.like("%{}%".format(port_server)),
                    DynamicModel.port_time <= end_time, 
                    DynamicModel.port_time >= start_time,
                    DynamicModel.port_new <= new,
                    DynamicModel.port_new >= 0,
                    DynamicModel.port_user.like("%{}%".format(user)),
                ).order_by(DynamicModel.port_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.port_domain.like("%{}%".format(port_domain)),
                    DynamicModel.port_ip.like("%{}%".format(port_ip)),
                    DynamicModel.port_port.like("%{}%".format(port_port)),
                    DynamicModel.port_server.like("%{}%".format(port_server)),
                    DynamicModel.port_time <= end_time, 
                    DynamicModel.port_time >= start_time,
                    DynamicModel.port_new <= new,
                    DynamicModel.port_new >= 0,
                    DynamicModel.port_user.like("%{}%".format(user)),
                ).count()
        else:
            query = db.session.query(
                    DynamicModel.port_domain, 
                    DynamicModel.port_ip, 
                    DynamicModel.port_port,
                    DynamicModel.port_server,
                    DynamicModel.port_time,
                    DynamicModel.port_user,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.port_domain, 
                    DynamicModel.port_ip, 
                    DynamicModel.port_port,
                    DynamicModel.port_server,
                    DynamicModel.port_time,
                    DynamicModel.port_new <= new,
                    DynamicModel.port_new >= 0,
                    DynamicModel.port_user == str(current_user),
                ).order_by(DynamicModel.port_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.port_domain, 
                    DynamicModel.port_ip, 
                    DynamicModel.port_port,
                    DynamicModel.port_server,
                    DynamicModel.port_time,
                    DynamicModel.port_new <= new,
                    DynamicModel.port_new >= 0,
                    DynamicModel.port_user == str(current_user),
                ).count()

    else:
        if(is_admin()):
            query = db.session.query(DynamicModel.port_new,DynamicModel.port_domain, DynamicModel.port_ip, DynamicModel.port_port,DynamicModel.port_server,DynamicModel.port_time,DynamicModel.port_user, Target.target_name).join(Target,Target.id == DynamicModel.port_target).order_by(DynamicModel.port_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.count()
        else:
            query = db.session.query(DynamicModel.port_new,DynamicModel.port_domain, DynamicModel.port_ip, DynamicModel.port_port,DynamicModel.port_server,DynamicModel.port_time,DynamicModel.port_user, Target.target_name).join(Target,Target.id == DynamicModel.port_target).filter(DynamicModel.port_user == str(current_user)).order_by(DynamicModel.port_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).count()

    content = []
    #转换成dict
    for q in query.items:
        content.append(queryToDict(q))

    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('port.html',form = dict, segment=get_segment(request)  )