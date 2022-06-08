import requests
from apps.home.models import Weather, History
from apps import db
import datetime
from flask import jsonify, render_template
from flask_login import login_required
from apps import login_manager

api_key = "HUHJZKRNLZMHZXRLMKCHF5AT3"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

headers = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }


@login_required
def getInventory():
    r = requests.get('http://213.47.49.66:48080/api/inventory', headers=headers)
    if r.status_code == 200:
        # timestamp = str(datetime.datetime.now())
        # timestamp = timestamp[:-7]
        # inventory_list = r.json()
        #
        # for object in inventory_list:
        #     id_name = object["id"]
        #     type = object["type"]
        #     info = "getInventory"
        #     new_entry = History(id_name=id_name, timestamp=timestamp, type=type, info=info)
        #     db.session.add(new_entry)
        #     db.session.commit()

        return r.json(), 200

    return "No inventory available, please check connection", 404


@login_required
def getHistoryByID(id):
    if id == "all":
        entries = History.query.all()
    else:
        entries = History.query.filter_by(id_name=f"{id}").all()

    history = []
    for entry in entries:
        dictionary = entry.__dict__
        print(dictionary)
        del dictionary['_sa_instance_state']
        history.append(dictionary)

    if history:
        return jsonify(history), 200

    return "requested id not found", 404


# https://www.weatherapi.com/my/
# plu79815@zcrcd.com
# 1234asdf

# 33d72edc26bc44d294c135038220606


@login_required
def get_weather():
    complete_url = base_url + "Graz" + "?unitGroup=metric&key=" + api_key + "&contentType=json"
    r = requests.get(complete_url)
    if r.status_code == 200:
        weather_data = r.json()
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

        return weather_data, 200

    return "No weather data available", 404

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403
