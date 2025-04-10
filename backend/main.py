import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).parent.parent))

from backend.api.v1.routers.audio import router as audio_router
from backend.api.v1.routers.user import router as user_router
from backend.api.v1.routers.auth import router as auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(audio_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы HTTP
    allow_headers=["*"],  # Разрешает все заголовки
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000)
