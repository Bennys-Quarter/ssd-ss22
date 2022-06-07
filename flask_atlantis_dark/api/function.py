import json
import requests
from flask_atlantis_dark.apps.home.models import Weather, History
from apps import db

api_key = "HUHJZKRNLZMHZXRLMKCHF5AT3"
base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

headers = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }

def getInventory():  # ToDo yaml file does not match
    r = requests.get('http://213.47.49.66:48080/api/inventory', headers=headers)
    return r.json(), 200


def getHistoryByID():
    return "ToDo: look in db"

# https://www.weatherapi.com/my/
# plu79815@zcrcd.com
# 1234asdf

# 33d72edc26bc44d294c135038220606


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

        return last_entry , 200

    return "No weather data available", 404