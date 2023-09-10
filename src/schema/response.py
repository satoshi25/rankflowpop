from pydantic import BaseModel
from typing import List
from datetime import date


class UserResponse(BaseModel):
    id: int
    username: str


class UserLoginResponse(BaseModel):
    access_token: str


class KeywordResponse(BaseModel):
    keyword_id: int
    keyword: str


class ProductResponse(BaseModel):
    product_id: int
    product_url: str
    product_name: str


class UserProductKeywordResponse(BaseModel):
    user_product_keyword_id: int
    product: ProductResponse
    keyword: KeywordResponse


class UserProductListResponse(BaseModel):
    product_list: List[UserProductKeywordResponse]


class RankingResponse(BaseModel):
    record_id: int
    product_name: str
    keyword: str
    search_date: date
    ranking: int


class RankingListResponse(BaseModel):
    ranking_list: List[RankingResponse]
