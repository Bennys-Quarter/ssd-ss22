import requests
import json
import threading
import pause
from datetime import datetime
from flask_login import login_required
from flask import current_app

headers = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}
headers2 = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }


@login_required
def setStateByID(id, state):
    print(id,state)
    if find_ID(id):
        payload = {"id": id, "value": str(state)}
        r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers2, data=json.dumps(payload))
        if r.status_code == 200:
            return "successfully set state", 200
        else:
            return "state operation not successful", 500

    return "id not found", 404


@login_required
def setTimerByID(id, time, state):
    if find_ID(id):
        t = threading.Thread(target=timer, args=(id, time, state,), daemon=True)
        t.start()
        return "Successfully set timer", 200

    return "ID not found", 404


def timer(id, unix_time, state):
    payload = {"id": id, "value": state}
    pause.until(datetime.fromtimestamp(unix_time))
    print("Timer: set IO: " + id)
    r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers, data=json.dumps(payload))
    if r.status_code != 200:
        print("Error IO not setable")


def find_ID(id):
    for io in current_app.config["inventory"]:
        if io["id"] == id and io["type"] == "output":
            return True
    return False
