from app.home.dirb.models import Dirb
from app.home.target.models import *
from app.home.utils import *
from flask import render_template, request
from app import db
from flask_login import current_user
import math

#target目录总览
def dirb(DynamicModel = Dirb):
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
        dir_url = ""
        dir_status = ""
        dir_tool = ""
        dir_title = ""
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
            if('url' in i):
                dir_url = i.split("=")[1]
            if('tool' in i):
                dir_tool = i.split("=")[1]
            if('title' in i):
                dir_title = i.split("=")[1]
            if('status' in i):
                dir_status = i.split("=")[1]
            if('user' in i):
                user = i.split("=")[1]
            if('new' in i):
                new = 0 if i.split("=")[1] == 'true' else 1

        search = search.replace("&&", "%26%26")
        if(is_admin()):
            query = db.session.query(
                    DynamicModel.dir_base, 
                    DynamicModel.dir_status, 
                    DynamicModel.dir_length,
                    DynamicModel.dir_title,
                    DynamicModel.dir_time,
                    DynamicModel.dir_new,
                    DynamicModel.dir_user,
                    DynamicModel.dir_tool,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.dir_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.dir_base.like("%{}%".format(dir_url)),
                    DynamicModel.dir_status.like("%{}%".format(dir_status)),
                    DynamicModel.dir_title.like("%{}%".format(dir_title)),
                    DynamicModel.dir_tool.like("%{}%".format(dir_tool)),
                    DynamicModel.dir_time <= end_time, 
                    DynamicModel.dir_time >= start_time,
                    DynamicModel.dir_new <= new,
                    DynamicModel.dir_new >= 0,
                    DynamicModel.dir_user.like("%{}%".format(user)),
                ).order_by(DynamicModel.dir_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.dir_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.dir_base.like("%{}%".format(dir_url)),
                    DynamicModel.dir_status.like("%{}%".format(dir_status)),
                    DynamicModel.dir_title.like("%{}%".format(dir_title)),
                    DynamicModel.dir_tool.like("%{}%".format(dir_tool)),
                    DynamicModel.dir_time <= end_time, 
                    DynamicModel.dir_time >= start_time,
                    DynamicModel.dir_new <= new,
                    DynamicModel.dir_new >= 0,
                    DynamicModel.dir_user.like("%{}%".format(user)),
                ).count()
        else:
            query = db.session.query(
                    DynamicModel.dir_base, 
                    DynamicModel.dir_status, 
                    DynamicModel.dir_length,
                    DynamicModel.dir_title,
                    DynamicModel.dir_time,
                    DynamicModel.dir_new,
                    DynamicModel.dir_user,
                    DynamicModel.dir_tool,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.dir_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.dir_base.like("%{}%".format(dir_url)),
                    DynamicModel.dir_status.like("%{}%".format(dir_status)),
                    DynamicModel.dir_title.like("%{}%".format(dir_title)),
                    DynamicModel.dir_tool.like("%{}%".format(dir_tool)),
                    DynamicModel.dir_time <= end_time, 
                    DynamicModel.dir_time >= start_time,
                    DynamicModel.dir_new <= new,
                    DynamicModel.dir_new >= 0,
                    DynamicModel.dir_user==str(current_user),
                ).order_by(DynamicModel.dir_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.dir_base.like("%{}%".format(dir_url)),
                    DynamicModel.dir_status.like("%{}%".format(dir_status)),
                    DynamicModel.dir_title.like("%{}%".format(dir_title)),
                    DynamicModel.dir_tool.like("%{}%".format(dir_tool)),
                    DynamicModel.dir_time <= end_time, 
                    DynamicModel.dir_time >= start_time,
                    DynamicModel.dir_new <= new,
                    DynamicModel.dir_new >= 0,
                    DynamicModel.dir_user==str(current_user),
                ).count()

    else:
        if(is_admin()):
            query = db.session.query(DynamicModel.dir_tool,DynamicModel.dir_base, DynamicModel.dir_status, DynamicModel.dir_length,DynamicModel.dir_title,DynamicModel.dir_time,DynamicModel.dir_new,DynamicModel.dir_user, Target.target_name).join(Target,Target.id == DynamicModel.dir_target).order_by(DynamicModel.dir_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.count()
        else:
            query = db.session.query(DynamicModel.dir_tool,DynamicModel.dir_base, DynamicModel.dir_status, DynamicModel.dir_length,DynamicModel.dir_title,DynamicModel.dir_time,DynamicModel.dir_new,DynamicModel.dir_user, Target.target_name).join(Target,Target.id == DynamicModel.dir_target).filter(DynamicModel.dir_user == str(current_user)).order_by(DynamicModel.dir_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).count()

    content = []
    #转换成dict
    for q in query.items:
        content.append(queryToDict(q))

    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('dirb.html',form = dict, segment=get_segment(request)  )
