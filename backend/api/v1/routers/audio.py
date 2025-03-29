from email.policy import default
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Depends, Query, HTTPException
from starlette.responses import JSONResponse

from backend.dependencies import get_current_user, get_yandex_current_user
from backend.schemas.data_schemas import UserAuth, AudioResponse
from backend.services.audio_service import AudioService
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/audio",
    tags=["Аудио-загрузчик"],
)


@router.post("/upload_audio")
async def upload_audio(
        user: UserAuth = Depends(get_yandex_current_user),
        file: UploadFile = File(..., description="Загрузите аудио файл"),
        file_name: str = Form(..., description="Название файла без расширения")
):
    """
    Эндпоинт для загрузки аудиофайла.

    Параметры:
    - **user**: Текущий авторизованный пользователь, получаемый через зависимость `get_current_user`.
    - **file**: Аудиофайл, загружаемый пользователем. Требуется в формате multipart/form-data.
    - **file_name**: Название файла без расширения, передаваемое через форму.
    В процессе загрузки:
    - Сначала аудиофайл сохраняется с помощью `AudioService.save_audio`.
    - Если файл был успешно сохранён, информация о нем добавляется в базу данных с использованием метода `AudioService.add`.
    """

    audio = await AudioService.save_audio(file, file_name)
    if audio.file_path:
        await AudioService.add(user_id=user.id, file_name=file_name, file_path=audio.file_path)
        return JSONResponse(content=audio.model_dump(), status_code=200)
    else:
        return JSONResponse(content=audio.model_dump(), status_code=400)

@router.get("/get_audio_file_user/{user_id}")
async def get_audio_file_user(
    user_id: int,
    user: UserAuth = Depends(get_current_user),
) -> List[AudioResponse]:
    user = await UserService.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    audios = await AudioService.find_all(user_id=user.id)

    return audios
