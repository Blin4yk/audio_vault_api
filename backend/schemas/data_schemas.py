from pydantic import BaseModel

#-------Users-----#

class UserAuth(BaseModel):
    email: str
    password: str

#-------Audio-----#

class FileUploader(BaseModel):
    message: str
    file_path: str