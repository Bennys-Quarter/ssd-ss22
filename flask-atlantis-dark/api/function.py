import json
import requests

headers = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }


def getInventory():  # ToDo yaml file does not match
    r = requests.get('http://213.47.49.66:48080/api/inventory', headers=headers)
    return r.json(), 200


def getHistoryByID():  # ToDo: look in db
    pass

# https://www.weatherapi.com/my/
# plu79815@zcrcd.com
# 1234asdf

# 33d72edc26bc44d294c135038220606
def getWeather():
    r = requests.get("http://api.weatherapi.com/v1/current.json?key=33d72edc26bc44d294c135038220606&q=Graz&aqi=yes")
    if r.status_code == 200:
        return r.json()["current"], 200

    return "No weather data available", 404
