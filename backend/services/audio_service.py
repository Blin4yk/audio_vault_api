import os

from fastapi import UploadFile
from starlette.responses import JSONResponse
from pathlib import Path
from backend.repositories.sqlalc_models import Audio
from backend.schemas.data_schemas import FileUploader
from backend.services.base_service import BaseService


class AudioService(BaseService):
    model = Audio

    UPLOAD_DIRECTORY = "audio"

    @classmethod
    async def save_audio(cls, upload_file: UploadFile, file_name: str):
        try:
            # если папки нужной нет, то создастся
            os.makedirs(cls.UPLOAD_DIRECTORY, exist_ok=True)

            file = upload_file.file
            suffix = Path(upload_file.filename).suffix
            file_location = os.path.join(cls.UPLOAD_DIRECTORY, f"{file_name}{suffix}")

            with open(file_location, "wb") as f:
                f.write(file.read())

            return FileUploader(
                message=f"File {file_name} saved successfully",
                file_path=file_location
            )

        except Exception as e:
            return FileUploader(
                message=f"Error {str(e)}",
                file_path=""
            )
