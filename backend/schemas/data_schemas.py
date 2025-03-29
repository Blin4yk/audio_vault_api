from pydantic import BaseModel

#-------Users-----#

class UserAuth(BaseModel):
    username: str
    password: str

#-------Audio-----#

class FileUploader(BaseModel):
    message: str
    filename: str