from fastapi import Depends

from src.database.repository import UserRepository, ProductRepository
from src.schema.request import ProductKeywordRequest
from src.schema.response import UserProductKeywordResponse, ProductResponse, UserProductListResponse
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

    def create_user_product(
        self,
        access_token: str,
        request: ProductKeywordRequest
    ) -> UserProductKeywordResponse | dict:

        user_info: str | None = self.user_service.verify_access_token(access_token=access_token)

        if not user_info:
            return {"detail": "Not Authorized"}

        user_id: int = int(user_info.split(",")[1])

        user_product_create_response: UserProductKeywordResponse | None = self.prod_repo.create_user_product(
            user_id=user_id,
            request=request
        )
        if not user_product_create_response:
            return {"detail": "User Already Has 10 Product"}

        return user_product_create_response

    def update_user_product(
        self,
        access_token: str,
        user_product_keyword_id: int,
        request: ProductKeywordRequest
    ) -> UserProductKeywordResponse | dict:

        user_info: str | None = self.user_service.verify_access_token(access_token=access_token)

        if not user_info:
            return {"detail": "Not Authorized"}

        user_id: int = int(user_info.split(",")[1])

        user_product_update_response: UserProductKeywordResponse = self.prod_repo.update_user_product(
            user_product_keyword_id=user_product_keyword_id,
            user_id=user_id,
            request=request
        )

        return user_product_update_response

    def delete_user_product(
        self,
        access_token: str,
        user_product_keyword_id: int,
    ) -> ProductResponse | dict:

        user_info: str | None = self.user_service.verify_access_token(access_token=access_token)

        if not user_info:
            return {"status_code": 401, "detail": "Not Authorized"}

        user_id: int = int(user_info.split(",")[1])

        user_product_delete_response: ProductResponse | dict = self.prod_repo.delete_user_product(
            user_id=user_id,
            user_product_keyword_id=user_product_keyword_id,
        )

        return user_product_delete_response

    def get_user_product(
        self,
        access_token: str,
    ) -> UserProductListResponse | dict:
        user_info: str | None = self.user_service.verify_access_token(access_token=access_token)

        if not user_info:
            return {"status_code": 401, "detail": "Not Authorized"}

        user_id: int = int(user_info.split(",")[1])

        user_product_list: UserProductListResponse | None = self.prod_repo.get_user_product(
            user_id=user_id
        )
        if not user_product_list:
            return {"status_code": 400, "detail": "Product List Not Found"}

        return user_product_list
