from flask import Blueprint, jsonify, request, abort, current_app
from utils import auth, database, schemas, entity

states = Blueprint('states', __name__)

@states.route('/api/states/sensor/<_id_>', methods=['GET'])
@auth.token_auth.login_required
def get_sensor(_id_):
    current_entity = entity.Entity(_id_=_id_)
    if not (current_entity.load_from_id() and current_entity.get_type() == "sensor"):
        abort(404)
    return jsonify(current_entity.to_dict_state()), 200

@states.route('/api/states/input/<_id_>', methods=['GET'])
@auth.token_auth.login_required
def get_input(_id_):
    current_entity = entity.Entity(_id_=_id_)
    if not (current_entity.load_from_id() and current_entity.get_type() == "input"):
        abort(404)
    return jsonify(current_entity.to_dict_state()), 200

@states.route('/api/states/output/<_id_>', methods=['GET'])
@auth.token_auth.login_required
def get_output(_id_):
    current_entity = entity.Entity(_id_=_id_)
    if not (current_entity.load_from_id() and current_entity.get_type() == "output"):
        abort(404)
    return jsonify(current_entity.to_dict_state()), 200