import base64
import hashlib

from internal.config import settings


def pbkdf2_hmac(password: str, hash_name: str = 'sha256') -> str:
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name=hash_name,
        password=password.encode('utf-8'),
        salt=settings.SECRET_KEY.encode('utf-8'),
        iterations=100000,
        dklen=32,
    )
    return base64.b64encode(hashed_password).decode('utf-8').strip()
