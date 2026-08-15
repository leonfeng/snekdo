"""Authentication utilities for the snekdo application.

Provides JWT token generation/validation and password hashing.
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

try:
    import bcrypt
except ImportError:  # pragma: no cover
    bcrypt = None

try:
    from jose import jwt, JWTError
except ImportError:  # pragma: no cover
    jwt = None
    JWTError = Exception

# JWT settings
SECRET_KEY = os.environ.get("SNEKDO_JWT_SECRET_KEY", "snekdo-secret-key-change-me")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: The plaintext password to hash.

    Returns:
        The hashed password string.
    """
    if bcrypt is None:
        raise RuntimeError("bcrypt is not installed. Install with: pip install bcrypt")

    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash.

    Args:
        plain_password: The plaintext password to verify.
        hashed_password: The hash to verify against.

    Returns:
        True if the password matches, False otherwise.
    """
    if bcrypt is None:
        raise RuntimeError("bcrypt is not installed. Install with: pip install bcrypt")

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(user_id: str, expires_minutes: int = TOKEN_EXPIRE_MINUTES) -> str:
    """Create a JWT access token.

    Args:
        user_id: The user ID to embed in the token (sub claim).
        expires_minutes: Token expiration time in minutes.

    Returns:
        The encoded JWT token string.
    """
    if jwt is None:
        raise RuntimeError("python-jose is not installed. Install with: pip install python-jose")

    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> Optional[str]:
    """Decode a JWT access token and return the user ID.

    Args:
        token: The JWT token string.

    Returns:
        The user ID (sub claim) if valid, None otherwise.
    """
    if jwt is None:
        raise RuntimeError("python-jose is not installed. Install with: pip install python-jose")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
