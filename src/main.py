from fastapi import FastAPI, Depends, HTTPException

from src.schema.request import UserRequest, ProductRequest
from src.schema.response import UserResponse, UserLoginResponse, ProductResponse
from src.security import get_access_token
from src.service.product import ProductService
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


@app.post("/user/product")
def create_user_product_handler(
    request: ProductRequest,
    access_token: str = Depends(get_access_token),
    prod_service: ProductService = Depends()
) -> ProductResponse:

    product_response: ProductResponse | None = prod_service.create_user_product(
        request=request,
        access_token=access_token
    )
    if not product_response:
        raise HTTPException(status_code=401, detail="Not Authorized")

    return product_response


@app.on_event("shutdown")
async def shutdown_event():
    db.close()
