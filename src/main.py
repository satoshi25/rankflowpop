from fastapi import FastAPI, Depends, HTTPException

from src.schema.request import UserRequest
from src.schema.response import UserResponse
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
