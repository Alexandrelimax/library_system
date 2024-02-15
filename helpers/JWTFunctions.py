import jwt
from datetime import datetime, timedelta, timezone
from app import app

def generate_token(id, user):
    expiration_token = datetime.now(timezone.utc) + timedelta(hours=5)
    return jwt.encode({'id': id, 'username': user, 'exp': expiration_token}, app.config['secret'], algorithm='HS256')





