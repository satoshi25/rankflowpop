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


class ProductResponse(BaseModel):
    id: int
    product_url: str


class UserProductKeywordResponse(BaseModel):
    user_product_keyword_id: int
    product: ProductResponse
    keyword: KeywordResponse
