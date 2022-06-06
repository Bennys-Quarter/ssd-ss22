import requests
import json
import threading
import pause
from datetime import datetime

pause.until(datetime(2015, 8, 12, 2))

headers = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}
found_in_db = True

def getActorStateByID(id): # ToDo: really needed? Same function as state/{id}
    pass

def setStateByID(id, state): # ToDo: check switch is in db
    if found_in_db:
        payload = {"id": id, "value": state}
        r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            return "successfully set state", 200
        else:
            return "state operation not successful", 500

    return "id not found", 404

def timer(id, unix_time, state):
    payload = {"id": id, "value": state}
    pause.until(datetime.fromtimestamp(unix_time))
    print("Timer: set IO: " + id)
    r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers, data=json.dumps(payload))
    if r.status_code != 200:
        print("Error IO not setable")

def setTimerByID(id, time, state):
    if found_in_db: # ToDo: check id exists
        t = threading.Thread(target=timer, args=(id, time, state,), daemon=True)
        t.start()
        return "Successfully set timer", 200

    return "ID not found", 404
