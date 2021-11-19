# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
from pymysql import cursors
from app.home.scanconfig.models import Cronjob

from config import config_dict
from app import create_app, db
from multiprocessing import Process
from app.schedulertasks.controller import RunScheduler
from app.scan.conn import dbconn
import time

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 

Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )

if __name__ == "__main__":
    p = Process(target=RunScheduler,args=())
    p.start()
    conn, cursor = dbconn()
    sql = "UPDATE Cronjob set cronjob_pid=%s"
    cursor.execute(sql,(str(p.pid)))
    conn.commit()
    cursor.close()
    conn.close()
    app.run(host="0.0.0.0", port=5005, debug=False, threaded=True)
    