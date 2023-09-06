from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str


class UserLoginResponse(BaseModel):
    access_token: str
