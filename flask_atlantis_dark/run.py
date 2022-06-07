# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import time
from sys import exit

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
from flask_migrate import Migrate

from apps import create_app, db
from apps.config import config_dict

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'


try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
app.app.config["TEMPLATES_AUTO_RELOAD"] = True
Migrate(app, db)

if DEBUG:
    app.app.logger.info('DEBUG       = ' + str(DEBUG))
    app.app.logger.info('Environment = ' + get_config_mode)
    app.app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

    # Create admin to test with
    from apps.authentication.models import Users

    @app.app.before_first_request
    def create_admin():
        db.create_all()
        if db.session.query(Users).filter_by(username='admin').count() < 1:
            password = 'password'
            admin = Users(username='admin', password=password)
            db.session.add(admin)
            db.session.commit()

scheduler = BackgroundScheduler()


headers = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}
def updateSensorData():
    print("Update data on " + time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    sensors = ["test-sensor"]  # ToDo: use real sensors from db
    for sensor in sensors:
        url = "http://213.47.49.66:48080/api/states/sensor/" + sensor
        r = requests.get(url=url, headers=headers)
        print(r.json())
        # ToDo: save in db


if __name__ == "__main__":
    scheduler.add_job(func=updateSensorData, trigger="interval", seconds=5)
    #scheduler.start()

    app.run(debug=True, use_reloader=False)


#TODO: Make the Color choice functional again or remove it
