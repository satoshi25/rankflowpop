from pydantic import BaseModel, Field
from typing import List


class UserRequest(BaseModel):
    username: str
    password: str


class KeywordRequest(BaseModel):
    keyword: str


class ProductRequest(BaseModel):
    product_url: str
    keywords: List[KeywordRequest] = Field(..., max_items=2)

