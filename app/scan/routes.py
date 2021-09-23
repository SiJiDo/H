# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template,request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from app.scan.run import *

@blueprint.route('/startscan')
@login_required
def startscanroute():
    return startscan()

@blueprint.route('/stopscan')
@login_required
def stopscanroute():
    return stopscan()
