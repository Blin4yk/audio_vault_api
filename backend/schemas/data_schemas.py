from typing import Optional

from pydantic import BaseModel

#-----Users-----#

class UserAuth(BaseModel):
    email: str
    password: str

class UserUpdateSchema(BaseModel):
    email: Optional[str] = None

#-----Audio-----#
class AudioResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str

class FileUploader(BaseModel):
    message: str
    file_path: str

#-----Autorization-----#