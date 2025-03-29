from typing import Optional

from pydantic import BaseModel

#-------Users-----#

class UserAuth(BaseModel):
    email: str
    password: str

class UserUpdateSchema(BaseModel):
    email: Optional[str] = None

#-------Audio-----#

class FileUploader(BaseModel):
    message: str
    file_path: str