from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str