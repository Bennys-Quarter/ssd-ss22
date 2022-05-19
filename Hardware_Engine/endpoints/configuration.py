from flask import Blueprint, jsonify, request, abort, current_app
from utils import auth, schemas, configs

configuration = Blueprint('configuration', __name__)


@configuration.route('/api/configuration', methods=['POST'])
@auth.token_auth.login_required
def mqtt_config():
    conn_params = request.json
    if not schemas.validate(conn_params, schemas.schema_mqtt_configuration):
        abort(400)
    current_app.config["MQTT"] = conn_params
    configs.write_mqtt_config(conn_params, "./configuration.ini")
    return jsonify({"status": "OK"}), 200
