import jsonschema
from jsonschema import validate as validate_

schema_mqtt_configuration = {
    "type": "object",
    "properties": {
        "server": {"type": "string"},
        "port": {"type": "number"},
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
}

def validate(string, schema):
    if not string:
        return False
    try:
        validate_(instance=string, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        return False
    return True