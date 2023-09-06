from fastapi import FastAPI, Depends, HTTPException

from src.schema.request import UserRequest
from src.schema.response import UserResponse, UserLoginResponse
from src.service.user import UserService
from src.database.connect import db


app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"ping": "pong"}


@app.post("/user/sign-up", status_code=201)
def user_sign_up_handler(
    request: UserRequest,
    user_service: UserService = Depends(),
) -> UserResponse:

    user: UserResponse | None = user_service.create_user(username=request.username, password=request.password)

    if not user:
        raise HTTPException(status_code=400, detail="User Already Exist")

    db.close()
    return user


@app.post("/user/login", status_code=200)
def user_log_in_handler(
    request: UserRequest,
    user_service: UserService = Depends(),
) -> UserLoginResponse:

    access_token: UserLoginResponse | None = user_service.login_user(
        username=request.username,
        password=request.password
    )

    if not access_token:
        raise HTTPException(status_code=400, detail="Bad Request")

    return access_token
