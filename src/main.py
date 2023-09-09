from fastapi import FastAPI, Depends, HTTPException

from src.schema.request import UserRequest, ProductKeywordRequest
from src.schema.response import UserResponse, UserLoginResponse, UserProductKeywordResponse, ProductResponse
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


@app.post("/user/product", status_code=201)
def create_user_product_handler(
    request: ProductKeywordRequest,
    access_token: str = Depends(get_access_token),
    prod_service: ProductService = Depends()
) -> UserProductKeywordResponse:

    user_product_response: UserProductKeywordResponse | dict = prod_service.create_user_product(
        request=request,
        access_token=access_token
    )
    if type(user_product_response) != UserProductKeywordResponse:
        raise HTTPException(status_code=401, detail=user_product_response["detail"])

    return user_product_response


@app.patch("/user/product/{user_product_keyword_id}", status_code=200)
def update_user_product_handler(
    request: ProductKeywordRequest,
    user_product_keyword_id: int,
    access_token: str = Depends(get_access_token),
    prod_service: ProductService = Depends()
) -> UserProductKeywordResponse:

    user_product_response: UserProductKeywordResponse | dict = prod_service.update_user_product(
        user_product_keyword_id=user_product_keyword_id,
        request=request,
        access_token=access_token
    )
    if type(user_product_response) != UserProductKeywordResponse:
        raise HTTPException(status_code=401, detail=user_product_response["detail"])

    return user_product_response


@app.delete("/user/product/{user_product_keyword_id}", status_code=204)
def delete_user_product_handler(
    user_product_keyword_id: int,
    access_token: str = Depends(get_access_token),
    prod_service: ProductService = Depends()
) -> None:

    user_product_delete_response: UserProductKeywordResponse | dict = prod_service.delete_user_product(
        user_product_keyword_id=user_product_keyword_id,
        access_token=access_token
    )

    if type(user_product_delete_response) != ProductResponse:
        raise HTTPException(
            status_code=user_product_delete_response["status_code"],
            detail=user_product_delete_response["detail"]
        )


@app.on_event("shutdown")
async def shutdown_event():
    db.close()
