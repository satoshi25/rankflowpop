from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str


class ProductKeywordRequest(BaseModel):
    product_url: str
    product_name: str
    keyword: str
