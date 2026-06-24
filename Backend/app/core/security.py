import os
from datetime import datetime, timedelta
import jwt
from secrets import token_hex

# Simple fallback algorithm configs
SECRET_KEY = token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Mock simple secure hashing implementation (Using built-in hashlib safely)
import hashlib

def hash_password(password: str) -> str:
    """Creates a secure sha256 hex string block representation of plain text credentials."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)