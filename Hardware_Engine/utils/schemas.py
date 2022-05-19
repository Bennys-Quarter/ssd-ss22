import jsonschema
from jsonschema import validate as validate_

schema_mqtt_connection_parameters = {
    "type": "object",
    "properties": {
        "server": {"type": "string"},
        "port": {"type": "number"},
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
}

schema_register_entity = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "mqtt_topic": {"type": "string"},
        "address": {"type": "string"},
        "type": {"enum": ["sensor", "input", "output"]},
    },
    "required": ["id", "mqtt_topic", "type"]
}

schema_output_entity = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "value": {"type": "string"},
    },
    "required": ["id", "value"]
}


def validate(string, schema):
    if not string:
        return False
    try:
        validate_(instance=string, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True
