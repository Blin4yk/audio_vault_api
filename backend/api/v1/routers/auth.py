from fastapi import APIRouter, HTTPException, Response, Query
from requests_oauthlib import OAuth2Session

from backend.config import yandex_config, AUTHORIZATION_BASE_URL, TOKEN_URL
from backend.schemas.data_schemas import UserAuth
from backend.services.auth_service import get_password_hash, authenticate_user, create_access_token, \
    register_yandex_user
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post("/register", summary="Регистрация пользователя через email и пароль")
async def register_user(
    email: str = Query(..., detail="Введите почту"),
    password: str = Query(..., detail="Введите пароль")
):
    """
    Регистрация пользователя.

    Параметры:
    - **user_data**: Данные пользователя (`email и пароль`)
    **return**: Сообщение об успешной регистрации или ошибка
    """
    exiting_user = await UserService.find_one_or_none(email=email)
    if exiting_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = get_password_hash(password)
    await UserService.add(email=email, hash_password=hashed_password)
    return {"message": "User register successfully"}


@router.post("/login", summary="Авторизация пользователя")
async def login_user(
    response: Response,
    email: str = Query(..., detail="Введите почту"),
    password: str = Query(..., detail="Введите пароль")
):
    """
    Авторизация пользователя.

    Параметры:
    - **response**: Объект ответа для установки куки
    - **user_data**: Данные пользователя (`email и пароль`)
    - **return**: `Access-токен` в ответе и куки
    """
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout", summary="Выход из сессии")
async def logout_user(response: Response):
    """
    Выход из сессии пользователя.

    Параметры:
    - **response**: Объект ответа для удаления куки
    **return:** Сообщение об успешном выходе
    """
    response.delete_cookie("booking_access_token")
    return {"message": "User logged out successfully"}


@router.get("/authorize", summary="Получить ссылку на авторизацию Яндекс")
async def authorize():
    """
    Получение ссылки для авторизации через Яндекс.

    **return**: Ссылка на авторизацию в Яндексе
    """
    try:
        oauth = OAuth2Session(yandex_config.client_id, redirect_uri=yandex_config.redirect_uri)
        authorization_url, _ = oauth.authorization_url(AUTHORIZATION_BASE_URL)
        return {"authorization_url": authorization_url}
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка получения ссылки")


@router.post("/callback", summary="Обработка кода и добавление в базу данных пользователя")
async def callback(
        response: Response,
        code: str = Query(..., description="Код подтверждения из Яндекса"),
        password: str = Query(..., description="Пароль")
):
    """
    Обработка кода подтверждения и регистрация пользователя через Яндекс.
    Параметры:
    - **response**: Объект ответа для установки access-токена в куки
    - **code**: Код подтверждения из Яндекса
    - **password**: Пароль для создания учетной записи
    **return**: Access-токен в ответе и куки
    """
    try:
        oauth = OAuth2Session(yandex_config.client_id, redirect_uri=yandex_config.redirect_uri)
        token = oauth.fetch_token(TOKEN_URL, client_secret=yandex_config.client_secret, code=code)
        access_token = token.get("access_token")

        # Устанавливаем access_token в куки
        response.set_cookie(
            key="yandex_access_token",
            value=access_token,
            httponly=True,
        )

        await register_yandex_user(access_token, password)

        return {"access_token": access_token}
    except Exception:
        raise HTTPException(status_code=400, detail="Получите код")
