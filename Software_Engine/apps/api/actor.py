import requests
import json
import threading
import pause
from datetime import datetime
from flask_login import login_required
from flask import current_app
from apps.home.models import History
from apps import db
import datetime

headers = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}
headers2 = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }


@login_required
def setStateByID(id, state):

    if find_ID(id):
        payload = {"id": id, "value": str(state)}
        r = requests.post(current_app.config["hw_engine_url"] + '/api/control/output', headers=headers2, data=json.dumps(payload))
        if r.status_code == 200:
            print("successfully set state")
            info = "state set"
            timestamp = str(datetime.datetime.now())
            timestamp = timestamp[:-7]
            new_entry = History(id_name=id, timestamp=timestamp, type="output", info=info, data=state)
            db.session.add(new_entry)
            db.session.commit()
            return "successfully set state", 200
        else:
            print("state operation not successful", id, state)
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
    payload = {"id": id, "value": str(state)}
    pause.until(datetime.fromtimestamp(unix_time))
    r = requests.post(current_app.config["hw_engine_url"] + '/api/control/output', headers=headers2, data=json.dumps(payload))
    if r.status_code != 200:
        print("Error IO not setable")


def find_ID(id):
    for io in current_app.config["inventory"]:
        if io["id"] == id and io["type"] == "output":
            return True
    return False
