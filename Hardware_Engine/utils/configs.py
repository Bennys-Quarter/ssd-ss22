from configparser import ConfigParser
from flask import current_app

default_config = {"MQTT": {"server": "example.com", "port": 1883, "username": "", "password": ""}}


def write_mqtt_config(config, filename):
    config_object = ConfigParser()
    config_object["MQTT"] = current_app.config["MQTT"]
    with open(filename, 'w') as configuration:
        config_object.write(configuration)


def read_mqtt_config(filename):
    config_object = ConfigParser()
    config_object.read(filename)
    return config_object["MQTT"]
