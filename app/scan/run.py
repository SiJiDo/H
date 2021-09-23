from app.home.target.view import target
from app.home.target.models import Target
from time import sleep
from flask import render_template, request, redirect, url_for
from multiprocessing import Process
from app import db
import os

#开始扫描
def startscan():
    id = request.args.get('id')
    p = Process(target=startscan_process,args=(id,))
    p.start()
    db.session.query(Target).filter(Target.id == id).update({'target_pid':p.pid})
    db.session.commit()

    return redirect(url_for('home_blueprint.targetinforoute',id=id,message="开始扫描, 扫描进程为----" + str(p.pid)))

#暂停扫描
def stopscan():
    id = request.args.get('id')
    pid = ""
    try:
        target = db.session.query(Target).filter(Target.id == id).first()
        print(target)
        pid = target.target_pid
        os.system("kill " + str(pid))
        db.session.query(Target).filter(Target.id == id).update({'target_pid':0})
        db.session.commit()
    except Exception as e:
        return redirect(url_for('home_blueprint.targetinforoute',id=id,message="内部错误" + str(pid)))
    return redirect(url_for('home_blueprint.targetinforoute',id=id,message="停止扫描, 扫描进程为----" + str(pid)))


def startscan_process(id):
    while(1):
        print("test--1")
        sleep(5)
    return