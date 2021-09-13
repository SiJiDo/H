from app.home.target.models import Target
from app.home import utils
from re import T
from app.home import blueprint
from flask import render_template, request
from flask_login import login_required
from app import db
import math

def target(DynamicModel = Target):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else 10

    query = DynamicModel.query.order_by(DynamicModel.id).paginate(page, length)
    total_count = DynamicModel.query.count()

    content = []
    #转换成dict
    for q in query.items:
        content.append(utils.queryToDict(q))

    for i in content:
        i['domain_total_count'] = 0
    print(content)
    dict = {'content': content, 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template('target.html',form = dict)

def targetadd(DynamicModel = Target):
    return render_template('targetadd.html')
