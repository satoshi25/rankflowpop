from typing import List

from src.database.connect import db
from src.schema.request import ProductKeywordRequest
from src.schema.response import ProductResponse, KeywordResponse, UserProductKeywordResponse, UserProductListResponse, \
    RankingResponse, RankingListResponse


class UserRepository:
    def __init__(self):
        self.db = db
        self.cursor = db.cursor()

    def get_user_by_username(self, username: str) -> tuple:

        sql: str = "SELECT * FROM user WHERE username = %s;"
        self.cursor.execute(sql, (username,))
        user: tuple = self.cursor.fetchone()

        return user

    def get_user_by_user_id(self, user_id: int) -> tuple:

        sql: str = "SELECT * FROM user WHERE id = %s;"
        self.cursor.execute(sql, (user_id,))
        user: tuple = self.cursor.fetchone()

        return user

    def create_user(self, username: str, password: str) -> tuple:

        sql: str = "INSERT INTO user (username, password) VALUES(%s, %s);"
        self.cursor.execute(sql, (username, password,))
        self.db.commit()

        insert_id: int = self.cursor.lastrowid

        user: tuple = self.get_user_by_user_id(user_id=insert_id)

        return user


class ProductRepository:
    def __init__(self):
        self.db = db
        self.cursor = db.cursor()
        self.sql_check_product: str = "SELECT * FROM product WHERE product_url = %s AND product_name = %s;"
        self.sql_check_keyword: str = "SELECT * FROM keyword WHERE keyword = %s;"
        self.sql_check_product_keyword: str = \
            ("SELECT * "
             "FROM product_keyword pk "
             "JOIN keyword k ON pk.keyword_id = k.id "
             "JOIN product p ON pk.product_id = p.id "
             "WHERE p.id = %s AND k.id = %s;")

        self.sql_insert_product: str = "INSERT INTO product (product_url, product_name) VALUES(%s, %s);"
        self.sql_insert_keyword: str = "INSERT INTO keyword (keyword) VALUES(%s);"
        self.sql_insert_product_keyword: str = \
            "INSERT INTO product_keyword (product_id, keyword_id) VALUES(%s, %s);"

        self.sql_check_user_product_keyword: str = \
            ("SELECT * "
             "FROM user_product_keyword upk "
             "JOIN user u ON upk.user_id = u.id "
             "JOIN product_keyword pk ON upk.product_keyword_id = pk.id "
             "JOIN keyword k ON pk.keyword_id = k.id "
             "JOIN product p ON pk.product_id = p.id "
             "WHERE u.id = %s AND p.id = %s AND k.id = %s;")

        self.sql_insert_user_product_keyword: str = \
            "INSERT INTO user_product_keyword (user_id, product_keyword_id) VALUES (%s, %s);"
        self.sql_update_user_product_keyword: str = \
            "UPDATE user_product_keyword SET product_keyword_id = %s WHERE id = %s AND user_id = %s;"

        self.sql_delete_check_user_product_keyword: str = "SELECT * FROM user_product_keyword WHERE id = %s;"
        self.sql_delete_user_product_keyword: str = "DELETE FROM user_product_keyword WHERE id = %s;"
        self.sql_get_user_product_keyword: str = "SELECT upk.id, p.id, p.product_url, p.product_name, k.id, k.keyword FROM user_product_keyword as upk JOIN product_keyword pk ON upk.product_keyword_id = pk.id JOIN product p ON pk.product_id = p.id JOIN keyword k ON pk.keyword_id = k.id WHERE upk.user_id = %s;"

    def create_user_product(
        self,
        user_id: int,
        request: ProductKeywordRequest
    ) -> UserProductKeywordResponse | None:

        self.cursor.execute("SELECT COUNT(*) FROM user_product_keyword WHERE user_id = %s;", (user_id,))
        count: int = self.cursor.fetchone()[0]

        if count < 10:
            self.cursor.execute(self.sql_check_product, (request.product_url, request.product_name,))
            product_raw: tuple = self.cursor.fetchone()
            if not product_raw:
                self.cursor.execute(self.sql_insert_product, (request.product_url, request.product_name))
                self.db.commit()
                product_id: int = self.cursor.lastrowid
            else:
                product_id: int = product_raw[0]

            self.cursor.execute(self.sql_check_keyword, (request.keyword,))
            keyword_raw: tuple = self.cursor.fetchone()
            if not keyword_raw:
                self.cursor.execute(self.sql_insert_keyword, (request.keyword,))
                self.db.commit()
                keyword_id: int = self.cursor.lastrowid
            else:
                keyword_id: int = keyword_raw[0]

            self.cursor.execute(self.sql_check_product_keyword, (product_id, keyword_id,))
            product_keyword_raw: tuple = self.cursor.fetchone()
            if not product_keyword_raw:
                self.cursor.execute(self.sql_insert_product_keyword, (product_id, keyword_id,))
                self.db.commit()
                product_keyword_id: int = self.cursor.lastrowid
            else:
                product_keyword_id: int = product_keyword_raw[0]

            self.cursor.execute(self.sql_check_user_product_keyword, (user_id, product_id, keyword_id))
            user_product_keyword_raw: tuple = self.cursor.fetchone()
            if not user_product_keyword_raw:
                self.cursor.execute(self.sql_insert_user_product_keyword, (user_id, product_keyword_id,))
                self.db.commit()
                user_product_keyword_id: int = self.cursor.lastrowid
            else:
                user_product_keyword_id: int = user_product_keyword_raw[0]

            keyword_response: KeywordResponse = KeywordResponse(
                keyword_id=keyword_id,
                keyword=request.keyword
            )

            product_response: ProductResponse = ProductResponse(
                product_id=product_id,
                product_url=request.product_url,
                product_name=request.product_name
            )

            user_product_response: UserProductKeywordResponse = UserProductKeywordResponse(
                user_product_keyword_id=user_product_keyword_id,
                product=product_response,
                keyword=keyword_response
            )
            return user_product_response
        else:
            return None

    def update_user_product(
        self,
        user_id: int,
        user_product_keyword_id: int,
        request: ProductKeywordRequest,
    ):

        self.cursor.execute(self.sql_check_product, (request.product_url, request.product_name))
        product_raw: tuple = self.cursor.fetchone()

        if not product_raw:
            self.cursor.execute(self.sql_insert_product, (request.product_url, request.product_name))
            self.db.commit()
            product_id: int = self.cursor.lastrowid
        else:
            product_id: int = product_raw[0]

        self.cursor.execute(self.sql_check_keyword, (request.keyword,))
        keyword_raw: tuple = self.cursor.fetchone()

        if not keyword_raw:
            self.cursor.execute(self.sql_insert_keyword, (request.keyword,))
            self.db.commit()
            keyword_id: int = self.cursor.lastrowid
        else:
            keyword_id: int = keyword_raw[0]

        self.cursor.execute(self.sql_check_product_keyword, (product_id, keyword_id,))
        product_keyword_raw: tuple = self.cursor.fetchone()
        if not product_keyword_raw:
            self.cursor.execute(self.sql_insert_product_keyword, (product_id, keyword_id,))
            self.db.commit()
            product_keyword_id: int = self.cursor.lastrowid
        else:
            product_keyword_id: int = product_keyword_raw[0]
        self.cursor.execute(self.sql_update_user_product_keyword, (product_keyword_id, user_product_keyword_id, user_id))
        self.db.commit()

        response_keyword = KeywordResponse(id=keyword_id, keyword=request.keyword)
        product_response: ProductResponse = ProductResponse(
            product_id=product_id,
            product_url=request.product_url,
            product_name=request.product_name
        )

        user_product_update_response: UserProductKeywordResponse = UserProductKeywordResponse(
            user_product_keyword_id=user_product_keyword_id,
            product=product_response,
            keyword=response_keyword
        )

        return user_product_update_response

    def delete_user_product(
        self,
        user_id: int,
        user_product_keyword_id: int,
    ) -> ProductResponse | dict:
        self.cursor.execute(self.sql_delete_check_user_product_keyword, (user_product_keyword_id,))
        check_user_product_keyword: tuple = self.cursor.fetchone()

        if not check_user_product_keyword:
            return {"status_code": 404, "detail": "Product Not Found"}
        elif check_user_product_keyword[1] != user_id:
            return {"status_code": 400, "detail": "Bad Request"}
        else:
            self.cursor.execute(self.sql_delete_user_product_keyword, (user_product_keyword_id,))
            self.db.commit()

            user_delete_result: ProductResponse = ProductResponse(
                product_id=user_product_keyword_id,
                product_url=f"{user_product_keyword_id}",
                product_name=f"{user_product_keyword_id}"
            )

        return user_delete_result

    def get_user_product(
        self,
        user_id: int,
    ) -> UserProductListResponse | None:
        self.cursor.execute(self.sql_get_user_product_keyword, (user_id,))
        user_product_tuple: tuple = self.cursor.fetchall()

        if len(user_product_tuple) == 0:
            return None
        user_get_response_list: List[UserProductKeywordResponse] = []
        for user_product in user_product_tuple:
            product: ProductResponse = ProductResponse(
                product_id=user_product[1],
                product_url=user_product[2],
                product_name=user_product[3]
            )
            keyword: KeywordResponse = KeywordResponse(
                keyword_id=user_product[4],
                keyword=user_product[5]
            )
            user_product_keyword: UserProductKeywordResponse = UserProductKeywordResponse(
                user_product_keyword_id=user_product[0],
                product=product,
                keyword=keyword
            )
            user_get_response_list.append(user_product_keyword)
        get_product_list: UserProductListResponse = UserProductListResponse(
            product_list=user_get_response_list
        )

        return get_product_list


class RankingRepository:
    def __init__(self):
        self.db = db
        self.cursor = db.cursor()
        self.sql_select_ranking = (
            "SELECT r.id, upk.user_id, upk.product_keyword_id, r.search_date, r.ranking "
            "FROM (SELECT id, user_product_keyword_id, search_date, ranking, "
            "ROW_NUMBER() OVER(PARTITION BY user_product_keyword_id ORDER BY search_date DESC) "
            "AS row_num FROM record) r "
            "JOIN user_product_keyword upk ON upk.id = r.user_product_keyword_id "
            "WHERE r.row_num = 1 AND upk.user_id = %s;"
        )
        self.sql = (
            "SELECT sub.id, sub.product_name, sub.keyword, sub.search_date, sub.ranking "
            "FROM ("
            "SELECT r.id, p.product_name, k.keyword, r.search_date, r.ranking FROM record as r "
            "JOIN user_product_keyword upk ON r.user_product_keyword_id = upk.id "
            "JOIN product_keyword pk ON upk.product_keyword_id = pk.id "
            "JOIN product p ON pk.product_id = p.id "
            "JOIN keyword k ON pk.keyword_id = k.id "
            "WHERE upk.user_id = %s "
            "ORDER BY r.id DESC "
            "LIMIT 10) as sub "
            "ORDER BY sub.ranking ASC;"
        )

    def get_product_ranking(
        self,
        user_id: int,
    ) -> RankingListResponse | None:
        self.cursor.execute(self.sql, (user_id,))
        products_ranking_list: tuple = self.cursor.fetchall()

        if len(products_ranking_list) == 0:
            return None

        ranking_response_list: List[RankingResponse] = []
        for products_ranking in products_ranking_list:
            ranking: RankingResponse = RankingResponse(
                record_id=products_ranking[0],
                product_name=products_ranking[1],
                keyword=products_ranking[2],
                search_date=products_ranking[3],
                ranking=products_ranking[4]
            )
            ranking_response_list.append(ranking)
        ranking_list_response: RankingListResponse = RankingListResponse(
            ranking_list=ranking_response_list
        )
        return ranking_list_response
