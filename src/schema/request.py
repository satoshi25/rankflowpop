from pydantic import BaseModel, validator
import re


class UserRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def check_username(cls, v):
        name = re.compile("(?=.*[a-z])(?!.*[~!@#$%^&*()_+=\\-/.,])[A-Za-z\\d]{4,}")
        if not name.match(v):
            raise ValueError("Invalid Username")
        return v

    @validator("password")
    def check_password(cls, v):
        ps = re.compile("(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{4,}")
        if not ps.match(v):
            raise ValueError("Invalid Password")
        return v


class ProductKeywordRequest(BaseModel):
    product_url: str
    product_name: str
    store_name: str
    keyword: str

    @validator("product_name", "store_name", "keyword")
    def check_empty(cls, v):
        v = v.strip()
        if v == "":
            raise ValueError("Field Cannot Be Empty")
        return v
