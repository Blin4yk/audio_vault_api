from typing import Dict, Any

from sqlalchemy import select
from starlette import status
from starlette.exceptions import HTTPException

from backend.config import async_session_maker
from backend.repositories.sqlalc_models import User
from backend.services.base_service import BaseService


class UserService(BaseService):
    model = User

