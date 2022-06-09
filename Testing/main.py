#!/usr/bin/env python3

import requests
import json

headers = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }

headers2 = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}
payload = {"id": "test-k0", "value": "1"}


if __name__ == '__main__':
    f = open("results.txt", 'w')

    print("########### Starting HW engine tests ##########")

    f.write("######### Hardware engine state 200 tests #########\n")
    r = requests.get('http://213.47.49.66:48080/api/inventory', headers=headers)
    f.write("{} -> inventory\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/output/test-k0', headers=headers2)
    f.write("{} -> states/output\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/sensor/test-sensor', headers=headers2)
    f.write("{} -> states/sensor\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/input/test-i0', headers=headers2)
    f.write("{} -> states/input\n".format("success" if r.status_code == 200 else "fail"))
    r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers, data=json.dumps(payload))
    f.write("{} -> control/output\n".format("success" if r.status_code == 200 else "fail"))

    f.write("\n######## Hardware engine state error tests ########\n")
    r = requests.get('http://213.47.49.66:48080/api/inventory')
    f.write("{} -> inventory unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/output/not-a-IO', headers=headers2)
    f.write("{} -> states/output Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/output/not-a-IO')
    f.write("{} -> states/output unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/sensor/test-sensor')
    f.write("{} -> states/sensor unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/sensor/not-a-IO', headers=headers2)
    f.write("{} -> states/sensor Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/input/test-i0')
    f.write("{} -> states/input unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.get('http://213.47.49.66:48080/api/states/input/not-a-IO', headers=headers2)
    f.write("{} -> states/input Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    r = requests.post('http://213.47.49.66:48080/api/control/output', data=json.dumps(payload))
    f.write("{} -> control/output unauthorized access\n".format("success" if r.status_code == 401 else "fail"))
    r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers)
    f.write("{} -> control/output Invalid request\n".format("success" if r.status_code == 400 else "fail"))
    payload_err = {"id": "not-a-IO", "value": "1"}
    r = requests.post('http://213.47.49.66:48080/api/control/output', headers=headers, data=json.dumps(payload_err))
    f.write("{} -> control/output Entity does not exist\n".format("success" if r.status_code == 404 else "fail"))
    f.close()