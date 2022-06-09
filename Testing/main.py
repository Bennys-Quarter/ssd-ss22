#!/usr/bin/env python3

import requests
import json
import datetime
import time

headers = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }

headers2 = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}
payload = {"id": "test-k0", "value": "1"}

# Change me
hw_engine_url = "http://localhost:8080/"
sw_engine_url = "http://localhost:85/"

if __name__ == '__main__':
    f = open("results.txt", 'w')

    print("########### Starting HW engine tests ##########")

    f.write("######### Hardware engine state 200 tests #########\n")
    r = requests.get(hw_engine_url + 'api/inventory', headers=headers)
    f.write("{} -> inventory\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/output/test-k0', headers=headers2)
    f.write("{} -> states/output\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/sensor/test-sensor', headers=headers2)
    f.write("{} -> states/sensor\n".format("success" if r.status_code == 200 else "fail"))
    #r = requests.get(hw_engine_url + 'api/states/input/test-i0', headers=headers2)
    #f.write("{} -> states/input\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.post(hw_engine_url + 'api/control/output', headers=headers, data=json.dumps(payload))
    f.write("{} -> control/output\n".format("success" if r.status_code == 200 else "fail"))

    f.write("\n######## Hardware engine state error tests ########\n")
    r = requests.get(hw_engine_url + 'api/inventory')
    f.write("{} -> inventory unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/output/not-a-IO', headers=headers2)
    f.write("{} -> states/output Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/output/not-a-IO')
    f.write("{} -> states/output unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/sensor/test-sensor')
    f.write("{} -> states/sensor unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/sensor/not-a-IO', headers=headers2)
    f.write("{} -> states/sensor Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/input/test-i0')
    f.write("{} -> states/input unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get(hw_engine_url + 'api/states/input/not-a-IO', headers=headers2)
    f.write("{} -> states/input Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    r = requests.post(hw_engine_url + 'api/control/output', data=json.dumps(payload))
    f.write("{} -> control/output unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.post(hw_engine_url + 'api/control/output', headers=headers)
    f.write("{} -> control/output Invalid request\n".format("success" if r.status_code == 400 else "fail"))
    payload_err = {"id": "not-a-IO", "value": "1"}
    r = requests.post(hw_engine_url + 'api/control/output', headers=headers, data=json.dumps(payload_err))
    f.write("{} -> control/output Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))

    f.write("\n######## Software engine tests ########\n")

    tcs = [["api/user/login?username=admin&password=password", 200, "user login"],
           ["api/function/inventory", 200, "get inventory"],
           ["api/state/test-sensor", 200, "get sensor data"],
           ["api/state/test-k0", 200, "get actor state"],
           ["api/function/history/test-sensor", 200, "get history"],
           ["api/function/weather", 200, "get weather data"]
           ]

    s = requests.Session()
    for tc in tcs:
        r = s.get(sw_engine_url + tc[0])
        f.write("{} -> {}\n".format("success" if r.status_code == tc[1] else "fail", tc[2]))

    tc_actor = ["api/actor/test-k0/1", 200, "set actor state"]
    r = s.put(sw_engine_url + tc_actor[0])
    f.write("{} -> {}\n".format("success" if r.status_code == tc_actor[1] else "fail", tc_actor[2]))

    print("Wait for timer")
    time_delay = 5
    timestamp = int(datetime.datetime.now().timestamp()) + time_delay
    tc_timer = ["api/actor/light/timer?time=" + str(timestamp) + "&state=1", 200, "set timer (only succeeds with real HW)"]
    r = s.put(sw_engine_url + tc_actor[0])
    time.sleep(time_delay)
    actor_state = ["api/state/light", 200, "get actor state"]
    r = s.get(sw_engine_url + actor_state[0])
    f.write("{} -> {}\n".format("success" if r.json()["value"] == "1" else "fail", tc_timer[2]))

    tc_logout = ["api/user/logout", 200, "user logout"]
    r = s.get(sw_engine_url + tc_logout[0])
    f.write("{} -> {}\n".format("success" if r.status_code == tc_logout[1] else "fail", tc_logout[2]))

    f.close()
