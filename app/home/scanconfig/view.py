from app.home.target.models import Target
from app.home import utils
from flask import render_template
from app import db
import math

def scanmethod(DynamicModel = Target):
    return render_template('scanmethod.html')


