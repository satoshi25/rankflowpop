from fastapi import Depends
from typing import List

from src.database.repository import UserRepository, ProductRepository
from src.schema.request import ProductRequest
from src.schema.response import ProductResponse
from src.service.user import UserService


class ProductService:
    def __init__(
            self,
            user_repo: UserRepository = Depends(),
            user_service: UserService = Depends(),
            prod_repo: ProductRepository = Depends(),
    ):
        self.user_repo = user_repo
        self.user_service = user_service
        self.prod_repo = prod_repo

    def create_user_product(self, access_token: str, request: ProductRequest) -> ProductResponse | None:

        user_info: str | None = self.user_service.verify_access_token(access_token=access_token)

        if not user_info:
            return None

        user_id: int = int(user_info.split(",")[1])

        product_response: ProductResponse = self.prod_repo.create_user_product(user_id=user_id, request=request)

        return product_response
