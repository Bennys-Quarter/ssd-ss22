import requests
import json

headers = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}

# ToDo: Placeholder remove me with real data
type_IO = "sensor"
name_IO = "test-sensor"
found_in_db = True


def getStateByID(id):  # ToDo: find type and name in db

    if found_in_db:
        url = "http://213.47.49.66:48080/api/states/" + type_IO + "/" + name_IO
        r = requests.get(url=url, headers=headers)
        # ToDo: store new data in db with timestamp
        return json.dumps({"id": id, "value": r.json()["value"]}), 200

    return 'IO device not found', 404