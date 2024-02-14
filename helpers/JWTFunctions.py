import jwt
from datetime import  datetime, timedelta, timezone
from flask import jsonify
from app import app

class TokenDecodeError(Exception):
    pass

def generate_token(id, user):
    expiration_token = datetime.now(timezone.utc) + timedelta(hours=5)
    return jwt.encode({'id': id, 'username': user, 'exp': expiration_token}, app.config['secret'], algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config['secret'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenDecodeError('Token expirado')
    except jwt.InvalidTokenError:
        raise TokenDecodeError('Token inválido')


