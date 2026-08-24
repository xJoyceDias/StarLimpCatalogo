import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


load_dotenv()


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
JWT_SECRET = os.getenv("JWT_SECRET")


if not ADMIN_USERNAME or not ADMIN_PASSWORD or not JWT_SECRET:
    raise RuntimeError(
        "ADMIN_USERNAME, ADMIN_PASSWORD e JWT_SECRET "
        "precisam estar configurados no arquivo .env."
    )


ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60 * 8


security = HTTPBearer()


def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=ALGORITHM,
    )


def authenticate_admin(username: str, password: str) -> bool:
    return (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    )


def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username != ADMIN_USERNAME:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
            )

        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
        )