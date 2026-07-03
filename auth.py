import hashlib
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "IRCTC_SECRET"
ALGORITHM = "HS256"

# Simple hashing (no bcrypt issues)
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str):
    return hash_password(password) == hashed

def create_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)