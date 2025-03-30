from backend.repositories.sqlalc_models import User
from backend.services.base_service import BaseService


class UserService(BaseService):
    model = User
