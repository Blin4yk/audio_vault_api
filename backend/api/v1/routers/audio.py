from email.policy import default

from fastapi import APIRouter, UploadFile, File, Form, Depends
from starlette.responses import JSONResponse

from backend.dependencies import get_current_user
from backend.schemas.data_schemas import UserAuth
from backend.services.audio_service import AudioService

router = APIRouter(
    prefix="/auth",
    tags=["Аудио-загрузчик"],
)

@router.post("/upload_audio")
async def upload_audio(
    user: UserAuth = Depends(get_current_user),
    file: UploadFile = File(..., description="Загрузите аудио файл"),
    file_name: str = Form(..., description="Название файла без расширения")
):
    audio = await AudioService.save_audio(file, file_name)
    if audio.filename:
        await AudioService.add(user.id, file_name, audio.file_path)
        return JSONResponse(content=audio.model_dump(), status_code=200)
    else:
        return JSONResponse(content=audio.model_dump(), status_code=400)