from app.home.vuln.models import Vuln
from app.home.http.models import Http
from app.home.subdomain.models import Subdomain
from flask import render_template
from app import db
from flask_login import current_user
import math

#首页
def indexview():

    subdomain_total_count = db.session.query(Subdomain).count()
    subdomain_new_count = db.session.query(Subdomain).filter(Subdomain.subdomain_new == 0).count()
    subdomain_rate = format(subdomain_new_count / subdomain_total_count * 100, '.2f')

    http_total_count = db.session.query(Http).count()
    http_new_count = db.session.query(Http).filter(Http.http_new == 0).count()
    http_rate = format(http_new_count / http_total_count * 100, '.2f')

    vuln_total_count = db.session.query(Vuln).count()
    vuln_new_count = db.session.query(Vuln).filter(Vuln.vuln_new == 0).count()
    vuln_rate = format(vuln_new_count / vuln_total_count * 100, '.2f')

    content = {'subdomain_total_count' : subdomain_total_count, 'subdomain_new_count': subdomain_new_count, 'subdomain_rate': subdomain_rate,
                'http_total_count': http_total_count, 'http_new_count': http_new_count, 'http_rate': http_rate,
                'vuln_total_count': vuln_total_count, 'vuln_new_count': vuln_new_count, 'vuln_rate': vuln_rate
                }

    return render_template('index.html', form = content, segment='index')