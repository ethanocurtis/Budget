from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from passlib.hash import argon2
import jwt
from typing import Optional, Tuple
from .config import settings

def hash_password(pw: str) -> str:
    # Argon2 params can be tuned via env
    return argon2.using(
        time_cost=settings.argon2_time_cost,
        memory_cost=settings.argon2_memory_cost,
        parallelism=settings.argon2_parallelism,
    ).hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return argon2.verify(pw, hashed)

def _encode(payload: dict, ttl_seconds: int) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {**payload, "iat": int(now.timestamp()), "exp": int((now + timedelta(seconds=ttl_seconds)).timestamp())}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)

def create_access_token(sub: str) -> str:
    return _encode({"sub": sub, "type": "access"}, settings.jwt_access_ttl_min * 60)

def create_refresh_token(sub: str) -> str:
    return _encode({"sub": sub, "type": "refresh"}, settings.jwt_refresh_ttl_days * 24 * 3600)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
