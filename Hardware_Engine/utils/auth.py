from flask_httpauth import HTTPTokenAuth

tokens = {
    "token1": "user1",
    "token2": "user2"
}

token_auth = HTTPTokenAuth(scheme='Bearer')


@token_auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]
