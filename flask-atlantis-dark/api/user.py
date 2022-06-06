user = "admin"
user_password = "password"
token = "3c469e9d6c5875d37a43f353d4f88e61fcf812c66eee3457465a40b0da4153e0"


def login(username, password):
    if username == user and password == user_password:  # ToDo: real check in database
        return "{{token: {}}}".format(token), 200
    else:
        return "Invalid username/password supplied", 400


def logout():
    return "success", 200
