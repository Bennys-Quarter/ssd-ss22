from flask import Blueprint, jsonify
from utils import auth, database

inventory = Blueprint('inventory', __name__)


@inventory.route('/api/inventory', methods=['GET'])
@auth.token_auth.login_required
def get_inventory():
    return jsonify(database.get_inventory()), 200
