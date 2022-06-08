# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from apps.home import blueprint
from apps.home.models import History, Weather
from apps.api.function import get_weather
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import datetime

api_key = "HUHJZKRNLZMHZXRLMKCHF5AT3"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


def darw_temp_plot():
    timestamp = str(datetime.datetime.now())
    timestamp = timestamp[:-7]
    temperature = "0"
    info = "temperature update"
    new_entry = History(timestamp=timestamp, actuator_state='00000000',
                        data=temperature, info=info)  # For testing only remove in deployment! This information should be gathered from the hardware engine
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
