# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_migrate import Migrate
from sys import exit
from decouple import config

from apps.config import config_dict
from apps import create_app, db


# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
app.app.config["TEMPLATES_AUTO_RELOAD"] = True
Migrate(app, db)

if DEBUG:
    app.app.logger.info('DEBUG       = ' + str(DEBUG))
    app.app.logger.info('Environment = ' + get_config_mode)
    app.app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

    # Create admin to test with
    from apps.authentication.models import Users

    @app.app.before_first_request
    def create_admin():
        db.create_all()
        if db.session.query(Users).filter_by(username='admin').count() < 1:
            password = 'password'
            admin = Users(username='admin', password=password)
            db.session.add(admin)
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)


#TODO: Make the line chart take data
#TODO: Make the Color choice functional agian
#TODO: Define the tabel visualy according to the database entries
#DONE: Define a Model for the history table
#DONE: Delet uneccessary icons in app
#DONE: Make the Weather Card better