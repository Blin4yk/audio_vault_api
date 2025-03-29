from typing import Dict, Any

from starlette import status
from starlette.exceptions import HTTPException

from backend.repositories.sqlalc_models import User
from backend.services.base_service import BaseService


class UserService(BaseService):
    model = User

    # @classmethod
    # async def update(cls, db_user: User, update_data: Dict[str, Any]) -> User:
    #     """
    #     Обновляет данные пользователя
    #
    #     Args:
    #         db_user: Объект пользователя из БД
    #         update_data: Словарь с новыми данными {поле: значение}
    #
    #     Returns:
    #         Обновленный пользователь
    #
    #     Raises:
    #         HTTPException: Если обновление не удалось
    #     """
    #     try:
    #         # Обновляем только те поля, которые переданы в update_data
    #         for field, value in update_data.items():
    #             # Проверяем, существует ли атрибут у модели (для безопасности)
    #             if hasattr(db_user, field):
    #                 setattr(db_user, field, value)
    #             else:
    #                 raise HTTPException(
    #                     status_code=status.HTTP_400_BAD_REQUEST,
    #                     detail=f"Поле {field} не существует в модели пользователя"
    #                 )
    #
    #         # Сохраняем изменения в БД
    #         await db_user.save()
    #         await db_user.refresh()  # Обновляем данные из БД (если нужно)
    #
    #         return db_user
    #
    #     except Exception as e:
    #         # Логируем ошибку (можно добавить logger.error)
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail=f"Ошибка при обновлении пользователя: {str(e)}"
    #         )