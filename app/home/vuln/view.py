from app.home.vuln.models import Vuln
from app.home.target.models import *
from app.home.utils import *
from flask import render_template, request
from app import db
from flask_login import current_user
import math

#target目录总览
def vuln(DynamicModel = Vuln):
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
        vuln_url = ""
        vuln_info = ""
        vuln_level = ""
        vuln_tool = ""
        user = ""
        new = 1
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
            if('level' in i):
                vuln_level = i.split("=")[1]
            if('url' in i):
                vuln_url = i.split("=")[1]
            if('info' in i):
                vuln_info = i.split("=")[1]
            if('tool' in i):
                vuln_tool = i.split("=")[1]
            if('user' in i):
                user = i.split("=")[1]
            if('new' in i):
                new = 0 if i.split("=")[1] == 'true' else 1

        search = search.replace("&&", "%26%26")
        if(is_admin()):
            query = db.session.query(
                    DynamicModel.vuln_poc, 
                    DynamicModel.vuln_level, 
                    DynamicModel.vuln_info,
                    DynamicModel.vuln_time,
                    DynamicModel.vuln_tool,
                    DynamicModel.vuln_new,
                    DynamicModel.vuln_user,
                    DynamicModel.vuln_name,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.vuln_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.vuln_level.like("%{}%".format(vuln_level)),
                    DynamicModel.vuln_info.like("%{}%".format(vuln_info)),
                    DynamicModel.vuln_poc.like("%{}%".format(vuln_url)),
                    DynamicModel.vuln_tool.like("%{}%".format(vuln_tool)),
                    DynamicModel.vuln_time <= end_time, 
                    DynamicModel.vuln_time >= start_time,
                    DynamicModel.vuln_new <= new,
                    DynamicModel.vuln_new >= 0,
                    DynamicModel.vuln_user.like("%{}%".format(user)),
                ).order_by(DynamicModel.vuln_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.vuln_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.vuln_level.like("%{}%".format(vuln_level)),
                    DynamicModel.vuln_info.like("%{}%".format(vuln_info)),
                    DynamicModel.vuln_poc.like("%{}%".format(vuln_url)),
                    DynamicModel.vuln_tool.like("%{}%".format(vuln_tool)),
                    DynamicModel.vuln_time <= end_time, 
                    DynamicModel.vuln_time >= start_time,
                    DynamicModel.vuln_new <= new,
                    DynamicModel.vuln_new >= 0,
                    DynamicModel.vuln_user.like("%{}%".format(user)),
                ).count()
        else:
            query = db.session.query(
                    DynamicModel.vuln_poc, 
                    DynamicModel.vuln_level, 
                    DynamicModel.vuln_info,
                    DynamicModel.vuln_time,
                    DynamicModel.vuln_tool,
                    DynamicModel.vuln_new,
                    DynamicModel.vuln_user,
                    DynamicModel.vuln_name,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.dir_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.vuln_level.like("%{}%".format(vuln_level)),
                    DynamicModel.vuln_info.like("%{}%".format(vuln_info)),
                    DynamicModel.vuln_poc.like("%{}%".format(vuln_url)),
                    DynamicModel.vuln_tool.like("%{}%".format(vuln_tool)),
                    DynamicModel.vuln_time <= end_time, 
                    DynamicModel.vuln_time >= start_time,
                    DynamicModel.vuln_new <= new,
                    DynamicModel.vuln_new >= 0,
                    DynamicModel.vuln_user==str(current_user),
                ).order_by(DynamicModel.vuln_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.vuln_level.like("%{}%".format(vuln_level)),
                    DynamicModel.vuln_info.like("%{}%".format(vuln_info)),
                    DynamicModel.vuln_poc.like("%{}%".format(vuln_url)),
                    DynamicModel.vuln_tool.like("%{}%".format(vuln_tool)),
                    DynamicModel.vuln_time <= end_time, 
                    DynamicModel.vuln_time >= start_time,
                    DynamicModel.vuln_new <= new,
                    DynamicModel.vuln_new >= 0,
                    DynamicModel.vuln==str(current_user),
                ).count()

    else:
        if(is_admin()):
            query = db.session.query(DynamicModel.vuln_tool,DynamicModel.vuln_poc, DynamicModel.vuln_level, DynamicModel.vuln_info,DynamicModel.vuln_time,DynamicModel.vuln_new,DynamicModel.vuln_user,Target.target_name,DynamicModel.vuln_name).join(Target,Target.id == DynamicModel.vuln_target).order_by(DynamicModel.vuln_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.count()
        else:
            query = db.session.query(DynamicModel.vuln_tool,DynamicModel.vuln_poc, DynamicModel.vuln_level, DynamicModel.vuln_info,DynamicModel.vuln_time,DynamicModel.vuln_new,DynamicModel.vuln_user,Target.target_name,DynamicModel.vuln_name).join(Target,Target.id == DynamicModel.vuln_target).filter(DynamicModel.vuln_user == str(current_user)).order_by(DynamicModel.vuln_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).count()
    
    content = []
    #转换成dict
    for q in query.items:
        content.append(queryToDict(q))

    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('vuln.html',form = dict, segment=get_segment(request)  )
