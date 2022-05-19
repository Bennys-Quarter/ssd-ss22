from flask import Flask, jsonify, request, abort
from flask_mqtt import Mqtt
from utils import mqtt, configs

from endpoints.configuration import configuration
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False





app.register_blueprint(configuration)




@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.config["MQTT"] = configs.read_mqtt_config("configuration.ini")
    mqtt_client = mqtt.init(mqtt_conn_params=app.config["MQTT"])
    mqtt.loop_start(mqtt_client)
    app.run(host='127.0.0.1', threaded=True, port=8080, debug=False)