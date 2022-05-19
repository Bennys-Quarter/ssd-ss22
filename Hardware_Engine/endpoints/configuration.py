from flask import Blueprint, jsonify, request, abort, current_app
from utils import auth, schemas, configs, entity

configuration = Blueprint('configuration', __name__)


@configuration.route('/api/configuration', methods=['POST'])
@auth.token_auth.login_required
def mqtt_config_set():
    conn_params = request.json
    if not schemas.validate(conn_params, schemas.schema_mqtt_connection_parameters):
        abort(400)
    current_app.config["MQTT"] = conn_params
    configs.write_mqtt_config(conn_params, "./configuration.ini")
    return jsonify({"status": "OK"}), 200

@configuration.route('/api/configuration', methods=['GET'])
@auth.token_auth.login_required
def mqtt_config_get():
    return jsonify(current_app.config["MQTT"]), 200

@configuration.route('/api/configuration/register', methods=['POST'])
@auth.token_auth.login_required
def register_entity_():
    register_entity = request.json
    print(register_entity)
    if not schemas.validate(register_entity, schemas.schema_register_entity):
        abort(400)
    new_entity = entity.Entity(
        _id_= register_entity["id"],
        mqtt_topic= register_entity["mqtt_topic"],
        address = register_entity.get("address"),
        _type_= register_entity["type"]
    )
    if not new_entity.register():
        abort(409)
    return jsonify({"status": "OK"}), 200