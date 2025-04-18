from datetime import datetime, timezone

from fastapi import Depends, Request, HTTPException
from jose import jwt, JWTError

from backend.config import jwt_config, yandex_config
from backend.repositories.sqlalc_models import User
from backend.services.auth_service import jwt_token
from backend.services.user_service import UserService


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, jwt_config.secret_key, jwt_config.algorithm
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=401, detail="Token has expired")

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Token missing user ID")
    user = await UserService.find_by_id(int(user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.email != "admin@email.ru":
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return current_user


def get_yandex_token(request: Request):
    token = request.cookies.get("yandex_access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    return token


async def get_yandex_current_user(access_token: str = Depends(get_yandex_token)):
    token = jwt_token(access_token)

    try:
        payload = jwt.decode(token, yandex_config.client_secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    expire: str = payload.get("exp")

    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(status_code=401, detail="Token has expired")

    user_email: str = payload.get("email")

    if not user_email:
        raise HTTPException(status_code=400, detail="Token missing user email")

    user = await UserService.find_one_or_none(email=user_email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
