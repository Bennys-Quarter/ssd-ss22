from flask import Flask, jsonify, request, abort
from utils import mqtt, configs, database

from endpoints.configuration import configuration
from endpoints.inventory import inventory
from endpoints.control import control

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

app.register_blueprint(configuration)
app.register_blueprint(inventory)
app.register_blueprint(control)


@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400


@app.errorhandler(401)
def bad_request(e):
    return jsonify(error=str(e)), 401


@app.errorhandler(404)
def bad_request(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(409)
def bad_request(e):
    return jsonify(error=str(e)), 409


if __name__ == '__main__':
    database.init_db()
    app.config["MQTT"] = configs.read_mqtt_config("configuration.ini")
    mqtt_client = mqtt.init(mqtt_conn_params=app.config["MQTT"])
    app.mqtt_client = mqtt_client
    mqtt.loop_start(mqtt_client)
    app.run(host='127.0.0.1', threaded=True, port=8080, debug=False)
