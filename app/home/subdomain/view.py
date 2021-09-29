from app.home.subdomain.models import Subdomain
from app.home.target.models import *
from app.home.utils import *
from flask import render_template, request
from app import db
from flask_login import current_user
import math

#target目录总览
def subdomain(DynamicModel = Subdomain):
    # 接收参数
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else 10
    query = ""
    search = ""
    total_count = ""

    #查询
    search = request.args.get('search')
    print(search)
    if search != 'None' and search and '=' in search:
        target = ""
        start_time = "2021-01-01 00:00:00"
        end_time = "2099-01-01 00:00:00"
        user = ""
        subdomain_name = ""
        subdomain_ip = ""
        new = 1
        info = search.split("&&")
        for i in info:
            if('target' in i):
                target = i.split("=")[1]
            if('start_time' in i):
                start_time = i.split("=")[1]
            if('end_time' in i):
                end_time = i.split("=")[1]
            if('user' in i):
                user = i.split("=")[1]
            if('subdomain' in i):
                subdomain_name = i.split("=")[1]
            if('ip' in i):
                subdomain_ip = i.split("=")[1]
            if('new' in i):
                new = 0 if i.split("=")[1] == 'true' else 1
            print(i)

        search = search.replace("&&", "%26%26")
        if(is_admin()):
            query = db.session.query(
                    DynamicModel.id,
                    DynamicModel.subdomain_name, 
                    DynamicModel.subdomain_ip, 
                    DynamicModel.subdomain_tool,
                    DynamicModel.subdomain_info,
                    DynamicModel.subdomain_time,
                    DynamicModel.subdomain_user,
                    DynamicModel.subdomain_new, 
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.subdomain_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.subdomain_name.like("%{}%".format(subdomain_name)),
                    DynamicModel.subdomain_ip.like("%{}%".format(subdomain_ip)),
                    DynamicModel.subdomain_time <= end_time, 
                    DynamicModel.subdomain_time >= start_time,
                    DynamicModel.subdomain_new <= new,
                    DynamicModel.subdomain_new >= 0,
                    DynamicModel.subdomain_user.like("%{}%".format(user)),
                ).order_by(DynamicModel.subdomain_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.subdomain_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.subdomain_name.like("%{}%".format(subdomain_name)),
                    DynamicModel.subdomain_ip.like("%{}%".format(subdomain_ip)),
                    DynamicModel.subdomain_time <= end_time, 
                    DynamicModel.subdomain_time >= start_time,
                    DynamicModel.subdomain_new <= new,
                    DynamicModel.subdomain_new >= 0,
                    DynamicModel.subdomain_user.like("%{}%".format(user)),
                ).count()
        else:
            query = db.session.query(
                    DynamicModel.id,
                    DynamicModel.subdomain_name, 
                    DynamicModel.subdomain_ip, 
                    DynamicModel.subdomain_info,
                    DynamicModel.subdomain_time,
                    DynamicModel.subdomain_user,
                    DynamicModel.subdomain_tool,
                    DynamicModel.subdomain_new, 
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.subdomain_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.subdomain_name.like("%{}%".format(subdomain_name)),
                    DynamicModel.subdomain_ip.like("%{}%".format(subdomain_ip)),
                    DynamicModel.subdomain_time <= end_time, 
                    DynamicModel.subdomain_time >= start_time,
                    DynamicModel.subdomain_new <= new,
                    DynamicModel.subdomain_new >= 0,
                    DynamicModel.subdomain_user == str(current_user),
                ).order_by(DynamicModel.subdomain_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.subdomain_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.subdomain_name.like("%{}%".format(subdomain_name)),
                    DynamicModel.subdomain_ip.like("%{}%".format(subdomain_ip)),
                    DynamicModel.subdomain_time <= end_time, 
                    DynamicModel.subdomain_time >= start_time,
                    DynamicModel.subdomain_user,
                    DynamicModel.subdomain_new <= new,
                    DynamicModel.subdomain_new >= 0,
                    DynamicModel.subdomain_user == str(current_user),
                ).count()

    else:
        if(is_admin()):
            query = db.session.query(DynamicModel.subdomain_new, DynamicModel.id,DynamicModel.subdomain_name, DynamicModel.subdomain_tool, DynamicModel.subdomain_user, DynamicModel.subdomain_ip, DynamicModel.subdomain_info,DynamicModel.subdomain_time, Target.target_name).join(Target,Target.id == DynamicModel.subdomain_target).order_by(DynamicModel.subdomain_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.count()
        else:
            query = db.session.query(DynamicModel.subdomain_new, DynamicModel.id,DynamicModel.subdomain_name, DynamicModel.subdomain_tool, DynamicModel.subdomain_user, DynamicModel.subdomain_ip, DynamicModel.subdomain_info,DynamicModel.subdomain_time, Target.target_name).join(Target,Target.id == DynamicModel.subdomain_target).filter(DynamicModel.subdomain_user == str(current_user)).order_by(DynamicModel.subdomain_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).count()



    content = []
    #转换成dict
    for q in query.items:
        content.append(queryToDict(q))

    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('subdomain.html',form = dict, segment=get_segment(request))
