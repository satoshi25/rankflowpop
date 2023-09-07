from pydantic import BaseModel
from typing import List


class UserResponse(BaseModel):
    id: int
    username: str


class UserLoginResponse(BaseModel):
    access_token: str


class KeywordResponse(BaseModel):
    id: int
    keyword: str
    rule: str


class ProductResponse(BaseModel):
    id: int
    product_url: str
    keywords: List[KeywordResponse]


class CreateProductsResponse(BaseModel):
    products: List[ProductResponse]
