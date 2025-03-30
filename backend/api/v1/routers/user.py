
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from backend.dependencies import get_current_admin_user
from backend.repositories.sqlalc_models import User
from backend.schemas.data_schemas import UserUpdateSchema
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.get("/user/{user_id}")
async def get_user(user_id: int, admin: User = Depends(get_current_admin_user)):
    """ Получение информации о пользователях (доступно админу) """
    user = await UserService.find_by_id(model_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователя не существует")
    return user

@router.delete("/user/{user_id}")
async def delete_user(user_id: int, admin: User = Depends(get_current_admin_user)):
    """ Удаление пользователя (доступно админу) """
    delete = await UserService.delete(model_id=user_id)
    if not delete:
        raise HTTPException(status_code=404, detail="Пользователя не существует")
    return JSONResponse(status_code=200, content={"deleted": delete})

@router.patch("/user/{user_id}")
async def update_user(
    user_id: int,
    update_data: UserUpdateSchema,
    user: User = Depends(get_current_admin_user)
):
    """Изменение данных о пользователе"""
    update_dict = update_data.model_dump(exclude_unset=True)

    if not update_dict:
        raise HTTPException(400, detail="Нет данных для обновления")

    update = await UserService.update(model_id=user_id, update_data=update_dict)

    return update
