from app.home.http.models import Http
from app.home.target.models import *
from app.home.dirb.models import * 
from app.home.vuln.models import *
from app.home.utils import *
from flask import render_template, request
from app import db
from flask_login import current_user
import math

#target目录总览
def http(DynamicModel = Http):
    #确定是否已浏览
    action = request.args.get('action')       
    if action == 'see':
        id = request.args.get('id')
        db.session.query(DynamicModel).filter(DynamicModel.id == id).update({DynamicModel.http_see: True})
        db.session.commit()
    if action == 'unsee':
        id = request.args.get('id')
        db.session.query(DynamicModel).filter(DynamicModel.id == id).update({DynamicModel.http_see: True})
        db.session.commit()


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
        http_url = ""
        http_title = ""
        http_status = ""
        finger = ""
        user = ""
        new = 2
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
                http_url = i.split("=")[1]
            if('title' in i):
                http_title = i.split("=")[1]
            if('status' in i):
                http_status = i.split("=")[1]
            if('user' in i):
                user = i.split("=")[1]
            if('finger' in i):
                finger = i.split("=")[1]
            if('new' in i):
                new = 0 if i.split("=")[1] == 'true' else 2

        search = search.replace("&&", "%26%26")
        if(is_admin()):
            query = db.session.query(
                    DynamicModel.id,
                    DynamicModel.http_schema, 
                    DynamicModel.http_name, 
                    DynamicModel.http_title,
                    DynamicModel.http_status,
                    DynamicModel.http_length,
                    DynamicModel.http_screen,
                    DynamicModel.http_finger,
                    DynamicModel.http_time,
                    DynamicModel.http_see,
                    DynamicModel.http_new,
                    DynamicModel.http_user,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.http_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.http_name.like("%{}%".format(http_url)),
                    DynamicModel.http_title.like("%{}%".format(http_title)),
                    DynamicModel.http_status.like("%{}%".format(http_status)),
                    DynamicModel.http_finger.like("%{}%".format(finger)),
                    
                    DynamicModel.http_new >= 0,
                    DynamicModel.http_new <= new,
                    DynamicModel.http_time <= end_time, 
                    DynamicModel.http_time >= start_time,
                    DynamicModel.http_user.like("%{}%".format(str(user))),
                ).order_by(DynamicModel.http_see).order_by(DynamicModel.http_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.http_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.http_name.like("%{}%".format(http_url)),
                    DynamicModel.http_title.like("%{}%".format(http_title)),
                    DynamicModel.http_status.like("%{}%".format(http_status)),
                    DynamicModel.http_finger.like("%{}%".format(finger)),
                    DynamicModel.http_new >= 0,
                    DynamicModel.http_new <= new,
                    DynamicModel.http_time <= end_time, 
                    DynamicModel.http_time >= start_time,
                    DynamicModel.http_user.like("%{}%".format(str(user))),
                ).count()
        else:
            query = db.session.query(
                    DynamicModel.id,
                    DynamicModel.http_schema, 
                    DynamicModel.http_name, 
                    DynamicModel.http_title,
                    DynamicModel.http_status,
                    DynamicModel.http_length,
                    DynamicModel.http_screen,
                    DynamicModel.http_finger,
                    DynamicModel.http_time,
                    DynamicModel.http_see,
                    DynamicModel.http_new,
                    DynamicModel.http_user,
                    Target.target_name,
                ).join(
                    Target,
                    Target.id == DynamicModel.http_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.http_name.like("%{}%".format(http_url)),
                    DynamicModel.http_title.like("%{}%".format(http_title)),
                    DynamicModel.http_status.like("%{}%".format(http_status)),
                    DynamicModel.http_finger.like("%{}%".format(finger)),
                    DynamicModel.http_new >= new,
                    DynamicModel.http_new <= 2,
                    DynamicModel.http_time <= end_time, 
                    DynamicModel.http_time >= start_time,
                    DynamicModel.http_user==str(current_user),
                ).order_by(DynamicModel.http_see).order_by(DynamicModel.http_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            
            total_count = DynamicModel.query.join(
                Target,
                Target.id == DynamicModel.port_target
                ).filter(
                    Target.target_name.like("%{}%".format(target)),
                    DynamicModel.http_name.like("%{}%".format(http_url)),
                    DynamicModel.http_title.like("%{}%".format(http_title)),
                    DynamicModel.http_status.like("%{}%".format(http_status)),
                    DynamicModel.http_finger.like("%{}%".format(finger)),
                    DynamicModel.http_new >= new,
                    DynamicModel.http_new <= 2,
                    DynamicModel.http_time <= end_time, 
                    DynamicModel.http_time >= start_time,
                    DynamicModel.http_user.like("%{}%".format(str(current_user))),
                ).count()

    else:
        if(is_admin()):
            query = db.session.query(DynamicModel.id,DynamicModel.http_schema, DynamicModel.http_name, DynamicModel.http_title,DynamicModel.http_status,DynamicModel.http_length,DynamicModel.http_screen,DynamicModel.http_finger,DynamicModel.http_time,DynamicModel.http_see,DynamicModel.http_new,DynamicModel.http_user,Target.target_name,).join(Target,Target.id == DynamicModel.http_target).order_by(DynamicModel.http_see).order_by(DynamicModel.http_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.count()
        else:
            query = db.session.query(DynamicModel.id,DynamicModel.http_schema, DynamicModel.http_name, DynamicModel.http_title,DynamicModel.http_status,DynamicModel.http_length,DynamicModel.http_screen,DynamicModel.http_finger,DynamicModel.http_time,DynamicModel.http_see,DynamicModel.http_new,DynamicModel.http_user,Target.target_name,).join(Target,Target.id == DynamicModel.http_target).filter(DynamicModel.http_user == str(current_user)).order_by(DynamicModel.http_see).order_by(DynamicModel.http_time.desc()).order_by(DynamicModel.id.desc()).paginate(page, length)
            total_count = DynamicModel.query.filter(DynamicModel.target_user == str(current_user)).count()

    content = []
    #转换成dict
    for q in query.items:
        content.append(queryToDict(q))
    for i in content:
        i['dirb_count'] = Dirb.query.filter(Dirb.dir_http == str(i['id'])).count()
        i['vuln_count'] = Vuln.query.filter(Vuln.vuln_http == str(i['id'])).count()

    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length, 'search': search}
    return render_template('http.html',form = dict, segment=get_segment(request)  )


#target目录总览
def httpinfo(DynamicModel = Http):
    # 接收参数
    id = request.args.get('id')
    query = ""
    dir_page = int(request.args.get('dir_page')) if request.args.get('dir_page') else 1
    dir_length = int(request.args.get('dir_length')) if request.args.get('dir_length') else 10
    vuln_page = int(request.args.get('vuln_page')) if request.args.get('vuln_page') else 1
    vuln_length = int(request.args.get('vuln_length')) if request.args.get('vuln_length') else 10
    vuln = request.args.get('vuln')

    if(is_admin()):
        query = DynamicModel.query.filter(DynamicModel.id == id).first()
        # 查询敏感目录列表
        query_dirb = db.session.query(Dirb.dir_path, Dirb.dir_status, Dirb.dir_title,Dirb.dir_length,Dirb.dir_time,).filter(Dirb.dir_http == id,).paginate(dir_page, dir_length)
        query_vuln = db.session.query(Vuln.vuln_level, Vuln.vuln_info, Vuln.vuln_poc,Vuln.vuln_time,).filter(Vuln.vuln_http == id,).paginate(vuln_page, vuln_length)
        vuln_total_count = Vuln.query.filter(Vuln.vuln_http == id).count()
        dirb_total_count = Dirb.query.filter(Dirb.dir_http == id).count()
        
    else:
        query = DynamicModel.query.filter(DynamicModel.id == id).filter(DynamicModel.target_user == str(current_user)).order_by(DynamicModel.id).first()
        query_dirb = db.session.query(Dirb.dir_path, Dirb.dir_status, Dirb.dir_title,Dirb.dir_length,Dirb.dir_time,).filter(Dirb.dir_http == id, Dirb.dir_user == str(current_user)).paginate(dir_page, dir_length)
        query_vuln = db.session.query(Vuln.vuln_level, Vuln.vuln_info, Vuln.vuln_poc,Vuln.vuln_time,).filter(Vuln.vuln_http == id, Vuln.vuln_user == str(current_user)).paginate(vuln_page, vuln_length)
        vuln_total_count = Vuln.query.filter(Vuln.vuln_http == id,Dirb.dir_user == str(current_user)).count()
        dirb_total_count = Dirb.query.filter(Dirb.dir_http == id, Vuln.vuln_user == str(current_user)).count()
    
    dir_content = []
    for q in query_dirb.items:
        dir_content.append(queryToDict(q))
    vuln_content = []
    for q in query_vuln.items:
        vuln_content.append(queryToDict(q))
    
    dict = {'content': query,
            'query_dirb':dir_content,'dir_total_page': math.ceil(dirb_total_count / dir_length),'dir_total_count':dirb_total_count,'dir_page':dir_page,'dir_length':dir_length,
            'query_vuln':vuln_content,'vuln_total_page': math.ceil(vuln_total_count / vuln_length),'vuln_total_count':vuln_total_count,'vuln_page':vuln_page,'vuln_length':vuln_length,
            }
    return render_template('httpinfo.html', form=dict, id=id, vuln=vuln, segment=get_segment(request))