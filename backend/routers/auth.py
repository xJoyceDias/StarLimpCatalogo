from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from ..auth import authenticate_admin, create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Autenticação"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(data: LoginRequest):
    if not authenticate_admin(
        data.username,
        data.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
        )

    token = create_access_token(data.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }