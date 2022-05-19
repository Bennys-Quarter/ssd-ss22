from flask import Blueprint, jsonify, request, abort, current_app
from utils import auth, database, schemas, entity

control = Blueprint('control', __name__)

@control.route('/api/control/output', methods=['POST'])
@auth.token_auth.login_required
def set_control():
    control = request.json
    if not schemas.validate(control, schemas.schema_output_entity):
        abort(400)
    new_entity = entity.Entity(_id_=control["id"])
    if not new_entity.load_from_id():
        abort(404)
    new_entity.target_value = control["value"]
    current_app.mqtt_client.publish(new_entity.mqtt_topic, new_entity.target_value)
    new_entity.update()
    return jsonify({"status": "OK"}), 200
