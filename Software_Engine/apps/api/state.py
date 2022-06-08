import requests
from flask import jsonify
from flask_login import login_required
from apps.home.models import History
from apps import db

headers = {"Authorization": "Bearer jhQcOHRI3bFlBniEaPc7"}


@login_required
def getStateByID(id):

    entry = History.query.filter_by(id_name=id).first()

    if entry:
        type_IO = entry.type
        name_IO = entry.id_name
        url = "http://213.47.49.66:48080/api/states/" + type_IO + "/" + name_IO
        r = requests.get(url=url, headers=headers)
        info="getStateByID"
        new_entry = History(id_name=name_IO, type=type_IO, data=r.json()["value"], info=info)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"id": id, "value": r.json()["value"], "type": entry.type}), 200

    return 'IO device not found. Try to get the inventory first: ../api/function/inventory', 404
