# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - Benedikt Görgei
"""

from flask import jsonify
from flask_atlantis_dark.apps.authentication.models import Users
from flask_atlantis_dark.apps.authentication.util import verify_pass
from flask_login import (
    current_user,
    login_user,
    logout_user
)

token = "3c469e9d6c5875d37a43f353d4f88e61fcf812c66eee3457465a40b0da4153e0"


def login(username, password):

    # Locate user
    user = Users.query.filter_by(username=username).first()

    # Check the password
    if user and verify_pass(password, user.password):

        login_user(user)
        if current_user.is_authenticated:
            return jsonify("{{token: {}}}".format(token)), 200

    return "Invalid username/password supplied", 400


def logout():
    logout_user()
    return "successfully logged out", 200
