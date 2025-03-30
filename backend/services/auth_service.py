from datetime import datetime, timedelta

import requests
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from starlette.exceptions import HTTPException

from backend.config import jwt_config, yandex_config
from backend.services.user_service import UserService

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, jwt_config.secret_key, jwt_config.algorithm
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UserService.find_one_or_none(email=email)
    if not user and not verify_password(password, user.hash_password):
        return None

    return user


def jwt_token(token: str):
    jwt_url = "https://login.yandex.ru/info?format=jwt"
    headers = {"Authorization": f"OAuth {token}"}
    response = requests.get(jwt_url, headers=headers)
    return response.text


def user_info(jwt_token: str):
    payload = jwt.decode(jwt_token, yandex_config.client_secret, algorithms=["HS256"])
    dict_info = {
        "email": payload["email"],
        "exp": payload["exp"],
    }
    return dict_info


async def register_yandex_user(access_token: str, password: str):
    email = user_info(jwt_token(access_token))["email"]
    exiting_user = await UserService.find_one_or_none(email=email)
    if exiting_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = get_password_hash(password)
    await UserService.add(email=email, hash_password=hashed_password)
