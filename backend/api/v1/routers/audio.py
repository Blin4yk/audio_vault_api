from email.policy import default

from fastapi import APIRouter, UploadFile, File, Form
from starlette.responses import JSONResponse

from backend.services.audio_service import AudioService

router = APIRouter(
    prefix="/auth",
    tags=["Аудио-загрузчик"],
)

@router.post("/upload_audio")
async def upload_audio(
    file: UploadFile = File(..., description="Загрузите аудио файл"),
    file_name: str = Form(..., description="Название файла без расширения")
):
    return await AudioService.save_audio(file, file_name)
