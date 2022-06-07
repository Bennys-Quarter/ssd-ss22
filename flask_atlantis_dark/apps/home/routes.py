# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_atlantis_dark.apps import db
from flask_atlantis_dark.apps.home import blueprint
from flask_atlantis_dark.apps.home.models import History, Weather
from flask_atlantis_dark.api.function import get_weather
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
import json
import datetime

api_key = "HUHJZKRNLZMHZXRLMKCHF5AT3"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


#def weather_request():
    # complete_url = base_url + "Graz" + "?unitGroup=metric&key=" + api_key + "&contentType=json"
    # weather_data = requests.get(complete_url).json()
    # main = weather_data["currentConditions"]
    #
    # temperature = main["temp"]
    # windspeed = main["windspeed"]
    # humidity = main["humidity"]
    # weather_description = weather_data["description"]
    # weather_condition = main["conditions"]
    # icon = main["icon"]
    #
    # if not windspeed == "None": windspeed = str(0.1)
    #
    # new_entry = Weather(temperature=temperature, windspeed=windspeed, humidity=humidity,
    #                     weather_description=weather_description, icon=icon, weather_condition=weather_condition)
    # db.session.add(new_entry)
    # db.session.commit()

    #entries = Weather.query.order_by(Weather.id.desc())
    #last_entry = entries.first()

    # print(" Temperature (in celsius unit) = " +
    #       str(last_entry.temperature) +
    #       "\n windspeed (in m/s) = " +
    #       str(last_entry.windspeed) +
    #       "\n humidity (in percentage) = " +
    #       str(last_entry.humidity) +
    #       "\n description = " +
    #       str(last_entry.weather_description))
    #
    # return last_entry


def darw_temp_plot():
    timestamp = str(datetime.datetime.now())
    timestamp = timestamp[:-7]
    temperature = "0"
    new_entry = History(timestamp=timestamp, actuator_state='00000000',
                        temperature=temperature)  # For testing only remove in deployment! This information should be gathered from the hardware engine
    db.session.add(new_entry)
    db.session.commit()

    history = History.query.all()

    entries = Weather.query.order_by(Weather.id.desc()).limit(20)
    length = 1
    temp_values = []
    temp_number = []
    for en in entries:
        temp_values.append(float(en.temperature))
        temp_number.append(length)
        length += 1

    return temp_values, temp_number, history


@blueprint.route('/index')
@login_required
def index():
    #Weather.query.delete()  # Delete this line to make entries permanent
    _weather_data_json, _response_code = get_weather()

    entries = Weather.query.order_by(Weather.id.desc())
    weather_data = entries.first()


    tempdata, length, history = darw_temp_plot()
    return render_template('home/index.html', segment='index', weather_data=weather_data, tempdata=tempdata,
                           length=length, history=history)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
