from email.policy import default

from fastapi import APIRouter, UploadFile, File, Form, Depends
from starlette.responses import JSONResponse

from backend.dependencies import get_current_user
from backend.schemas.data_schemas import UserAuth
from backend.services.audio_service import AudioService

router = APIRouter(
    prefix="/audio",
    tags=["Аудио-загрузчик"],
)


@router.post("/upload_audio")
async def upload_audio(
        user: UserAuth = Depends(get_current_user),
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
