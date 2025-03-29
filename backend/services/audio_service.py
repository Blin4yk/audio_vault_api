import os

from starlette.responses import JSONResponse

from backend.database import async_session_maker
from backend.repositories.sqlalc_models import Audio
from backend.services.base_service import BaseService


class AudioService(BaseService):
    model = Audio

    UPLOAD_DIRECTORY = "audio"

    @classmethod
    async def save_audio(cls, file, file_name: str):
        try:
            # если папки нужной нет, то создастся
            os.makedirs(cls.UPLOAD_DIRECTORY, exist_ok=True)

            file_location = os.path.join(cls.UPLOAD_DIRECTORY, file_name)

            with open(file_location, "wb") as f:
                f.write(await file.read())

            return JSONResponse(
                content={"message": f"File {file_name} saved successfully", "file_location": file_location},
                status_code=200)

        except Exception as e:
            return JSONResponse({"message": f"Error {str(e)}", "file_location": None})

    @classmethod
    async def add_audio_in_db(cls, user_id: int, file_name: str, file_path: str):
        async with async_session_maker() as session:
            data = {
                "user_id": user_id,
                "file_name": file_name,
                "file_path": file_path,
            }
            await
