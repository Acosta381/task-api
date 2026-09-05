from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from core.config import settings

password_hash = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password : str, hashed_password : str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data : dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({'exp':expire, 'type':'access'})

    encode_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm='HS256'
    )

    return encode_jwt

def decode_access_token(token : str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def create_refresh_token(data : dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({'exp':expire, 'type':'refresh'})

    encode_jwt = jwt.encode(
        to_encode,
        settings.secret_key, algorithm='HS256'
    )

    return encode_jwt