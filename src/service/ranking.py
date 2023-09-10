from fastapi import Depends

from src.database.repository import RankingRepository
from src.schema.response import RankingListResponse
from src.service.user import UserService


class RankingService:
    def __init__(
        self,
        rank_repo: RankingRepository = Depends(),
        user_service: UserService = Depends(),
    ):
        self.rank_repo: RankingRepository = rank_repo
        self.user_service: UserService = user_service

    def get_product_ranking(
        self,
        access_token: str,
    ) -> RankingListResponse | dict:
        user_info: str | None = self.user_service.verify_access_token(access_token=access_token)

        if not user_info:
            return {"status_code": 401, "detail": "Not Authorized"}

        user_id: int = int(user_info.split(",")[1])

        product_ranking_list: RankingListResponse | None = self.rank_repo.get_product_ranking(user_id=user_id)

        if not product_ranking_list:
            return {"status_code": 404, "detail": "Product Ranking Not Found"}

        return product_ranking_list
