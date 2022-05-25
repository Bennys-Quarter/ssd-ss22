from flask_login import UserMixin

from apps import db, login_manager


class Weather(db.Model, UserMixin):

    __tablename__ = 'Weather'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.String(64))
    windspeed = db.Column(db.String(64))
    humidity = db.Column(db.String(64))
    icon = db.Column(db.String(64))
    weather_description = db.Column(db.String(512))
    weather_condition = db.Column(db.String(64))


