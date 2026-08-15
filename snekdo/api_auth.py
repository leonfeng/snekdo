"""Authentication endpoints for the snekdo FastAPI application."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from snekdo.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from snekdo.models import User
from snekdo.storage import StorageError, UserStorage


def _derive_users_path(storage_path: str | None) -> str:
    """Derive the users JSON file path from the todos storage path."""
    if storage_path is None:
        return str(Path.home() / ".snekdo" / "users.json")
    path = Path(storage_path)
    return str(path.with_name("users.json"))


# ---------------------------------------------------------------------------
# Pydantic request / response models
# ---------------------------------------------------------------------------


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Schema for logging in."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    """Response model for a registered user (no password hash)."""

    id: str
    username: str
    display_name: str
    email: str
    created_at: str

    @classmethod
    def from_user(cls, user: User) -> UserResponse:
        return cls(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            email=user.email,
            created_at=user.created_at,
        )


class TokenResponse(BaseModel):
    """Response model for login (JWT token)."""

    access_token: str
    token_type: str = "bearer"


# ---------------------------------------------------------------------------
# Token extraction helper
# ---------------------------------------------------------------------------


def _get_token(authorization: str | None = None) -> str | None:
    """Extract the JWT token from the Authorization header.

    Args:
        authorization: The raw Authorization header value.

    Returns:
        The token string, or None if not present.
    """
    if authorization is None:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0] != "Bearer":
        return None
    return parts[1]


# ---------------------------------------------------------------------------
# get_current_user dependency
# ---------------------------------------------------------------------------


def get_current_user_factory(storage_path: str | None = None):
    """Create a get_current_user dependency for the given storage path.

    Args:
        storage_path: Optional path to the storage file.

    Returns:
        A callable that can be used as a FastAPI dependency.
    """

    def _get_user_storage() -> UserStorage:
        return UserStorage(storage_path=_derive_users_path(storage_path))

    def get_current_user(
        user_storage: UserStorage = Depends(_get_user_storage),
        authorization: str | None = Header(default=None),
    ) -> User:
        """Get the current authenticated user from the JWT token.

        Raises:
            HTTPException: If the token is missing or invalid.
        """
        token = _get_token(authorization)
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = decode_access_token(token)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = user_storage.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    return get_current_user


# Default get_current_user (uses default storage path)
get_current_user = get_current_user_factory()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------


def create_auth_router(storage_path: str | None = None) -> APIRouter:
    """Create the authentication router with register and login endpoints.

    Args:
        storage_path: Optional path to the storage file. If provided, the
            user storage will use this path.
    """

    _get_current_user = get_current_user_factory(storage_path=storage_path)

    def _get_user_storage() -> UserStorage:
        return UserStorage(storage_path=_derive_users_path(storage_path))

    router = APIRouter()

    @router.post(
        "/api/v1/auth/register",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
    )
    async def register(
        user_data: UserCreate,
        user_storage: UserStorage = Depends(_get_user_storage),
    ) -> UserResponse:
        """Register a new user account."""
        hashed_password = hash_password(user_data.password)
        user = User(
            username=user_data.username,
            password_hash=hashed_password,
            created_at=datetime.now().isoformat(),
        )
        try:
            user_storage.add(user)
        except StorageError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e
        return UserResponse.from_user(user)

    @router.post("/api/v1/auth/login", response_model=TokenResponse)
    async def login(
        login_data: UserLogin,
        user_storage: UserStorage = Depends(_get_user_storage),
    ) -> TokenResponse:
        """Login with username and password."""
        user = user_storage.get(login_data.username)
        if user is None or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = create_access_token(user.id)
        return TokenResponse(access_token=token, token_type="bearer")

    return router
