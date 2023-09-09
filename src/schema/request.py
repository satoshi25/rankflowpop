from pydantic import BaseModel, Field
from typing import List


class UserRequest(BaseModel):
    username: str
    password: str


class ProductKeywordRequest(BaseModel):
    product_url: str
    keyword: str
