import jwt
from datetime import datetime, timedelta
from flask import request, jsonify, make_response
from functools import wraps

SECRET_KEY = 'nejaky nahodny retazaec'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return make_response(jsonify({'message': 'Token is missing!'}), 403)

        try:
            # Odstránenie prefixu 'Bearer ' z tokenu, ak je prítomný
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return make_response(jsonify({'message': 'Token has expired'}), 401)
        except jwt.InvalidTokenError:
            return make_response(jsonify({'message': 'Invalid token'}), 401)

        return f(*args, **kwargs)

    return decorated


class AuthUtility(object):

    @staticmethod
    def generate_token(username):
        exp = datetime.utcnow() + timedelta(hours=1)  # Token platný 1 hodinu
        return jwt.encode({'user': username, 'exp': exp}, SECRET_KEY, algorithm='HS256')