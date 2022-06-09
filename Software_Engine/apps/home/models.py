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


class History(db.Model, UserMixin):

    __tablename__ = 'History'

    id = db.Column(db.Integer, primary_key=True)
    id_name = db.Column(db.String(256))
    type = db.Column(db.String(64))
    timestamp = db.Column(db.String(64))
    actuator_state = db.Column(db.String(8))
    data = db.Column(db.String(64))
    info = db.Column(db.String(256))
