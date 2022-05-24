# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from apps.home import blueprint
from apps.home.models import Weather
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
import json

api_key = "HUHJZKRNLZMHZXRLMKCHF5AT3"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()

def weather_request():
    complete_url = base_url + "Graz" + "?unitGroup=metric&key=" + api_key + "&contentType=json"
    weather_data = requests.get(complete_url).json()
    main = weather_data["currentConditions"]

    temperature = main["temp"]
    windspeed = main["windspeed"]
    humidity = main["humidity"]
    weather_description = weather_data["description"]
    weather_condition = main["conditions"]
    icon = main["icon"]

    if not windspeed == "None": windspeed = str(0.1)

    new_entry = Weather(temperature=temperature, windspeed=windspeed, humidity=humidity,
                        weather_description=weather_description, icon=icon, weather_condition=weather_condition)
    db.session.add(new_entry)
    db.session.commit()

    entries = Weather.query.order_by(Weather.id.desc())
    last_entry = entries.first()

    print(" Temperature (in celsius unit) = " +
          str(last_entry.temperature) +
          "\n windspeed (in m/s) = " +
          str(last_entry.windspeed) +
          "\n humidity (in percentage) = " +
          str(last_entry.humidity) +
          "\n description = " +
          str(last_entry.weather_description))

    return last_entry


@blueprint.route('/index')
@login_required
def index():
    #Weather.query.delete()  # Delete this line to make entries permanent
    weather_data = weather_request()
    return render_template('home/index.html', segment='index', weather_data=weather_data)


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
