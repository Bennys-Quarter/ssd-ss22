# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db
from apps.home import blueprint
from apps.home.models import History, Weather
from apps.api.function import get_weather
from apps.api.actor import setStateByID
from flask import render_template, request,  flash, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import SubmitField
import json
import datetime

class PowerSwitchForm(FlaskForm):
    power_switch = SubmitField("ON")

api_key = "HUHJZKRNLZMHZXRLMKCHF5AT3"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print ('Clear table %s' % table)
        session.execute(table.delete())
    session.commit()


def darw_temp_plot():

    sensor_data = History.query.filter_by(id_name="test-sensor").order_by(History.id.desc()).limit(20)
    entries = Weather.query.order_by(Weather.id.desc()).limit(20)
    length = 0
    temp_values = []
    temp_number = []
    temp_time = []
    for en in sensor_data:
        if en.data:
            temp_values.append(round(float(en.data), 1))
            temp_number.append(en.timestamp[-8:])
            if length == 0:
                temp_time.append(en.timestamp[-8:])
            if length == 4:
                temp_time.append(en.timestamp[-8:])
            if length == 9:
                temp_time.append(en.timestamp[-8:])
            if length == 14:
                temp_time.append(en.timestamp[-8:])
            length += 1
    if len(temp_time) < 3:
        padding = 3 - len(temp_time)
        for i in range(padding):
            temp_time.append("")
    history = History.query.all()
    return temp_values, temp_number, temp_time, length, history,


@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    _weather_data_json, _response_code = get_weather()

    entries = Weather.query.order_by(Weather.id.desc())
    weather_data = entries.first()

    tempdata, temp_number, temp_time,length, history = darw_temp_plot()
    print(temp_time)
    print(tempdata)
    print(temp_number)
    return render_template('home/index.html', segment='index', weather_data=weather_data, tempdata=tempdata,
                           temp_number=json.dumps(temp_number), temp_time=temp_time, history=history, length=length)

@blueprint.route('/', methods=['GET', 'POST'])
def power():
    # Weather.query.delete()  # Delete this line to make entries permanent
    if request.method == 'POST':
        if request.form.get('action1') == 'ON':
            setStateByID('light', 1)
        elif request.form.get('action2') == 'OFF':
            setStateByID('light', 0)
        elif request.form.get('action2') == 'ON':
            setStateByID('test-k0', 1)
        elif request.form.get('action2') == 'OFF':
            setStateByID('test-k0', 0)

    return redirect(url_for('home_blueprint.index'))

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
