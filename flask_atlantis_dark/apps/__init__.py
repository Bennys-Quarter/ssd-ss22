# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

import connexion
import requests


db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication', 'home'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

headers = {'content-type': 'application/json',
           "Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"
           }

def create_app(config):
    app = connexion.App(__name__, specification_dir='api')
    app.add_api('User-API.yaml', base_path='/api')
    app.app.config.from_object(config)
    register_extensions(app.app)
    register_blueprints(app.app)
    configure_database(app.app)

    r = requests.get('http://213.47.49.66:48080/api/inventory', headers=headers)
    app.app.config["inventory"] = r.json()
    sensors = []
    for io in r.json():
        if io["type"] == "sensor":
            sensors.append(io["id"])
    app.app.config["sensors"] = sensors

    return app
