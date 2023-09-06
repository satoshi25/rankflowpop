from fastapi import FastAPI, Depends

from src.schema.request import UserRequest
from src.schema.response import UserResponse
from src.service.user import UserService


app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


@app.post("/user/sign-up")
def user_sign_up_handler(
    request: UserRequest,
    user_service: UserService = Depends(),
) -> UserResponse:

    hashed_password: str = user_service.hash_password(password=request.password)

    return UserResponse()
