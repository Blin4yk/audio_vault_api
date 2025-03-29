from fastapi import APIRouter, HTTPException, Response

from backend.schemas.data_schemas import UserAuth
from backend.services.auth_service import get_password_hash, authenticate_user, create_access_token
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post("/register")
async def register_user(user_data: UserAuth):
    exiting_user = await UserService.find_one_or_none(email=user_data.email)
    if exiting_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hash_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: UserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
