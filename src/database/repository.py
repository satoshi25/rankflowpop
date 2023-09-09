from typing import List

from src.database.connect import db
from src.schema.request import ProductKeywordRequest
from src.schema.response import ProductResponse, KeywordResponse, UserProductKeywordResponse


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
        self.sql_check_product: str = "SELECT * FROM product WHERE product_url = %s;"
        self.sql_check_keyword: str = "SELECT * FROM keyword WHERE keyword = %s;"
        self.sql_check_product_keyword: str = \
            ("SELECT * "
             "FROM product_keyword pk "
             "JOIN keyword k ON pk.keyword_id = k.id "
             "JOIN product p ON pk.product_id = p.id "
             "WHERE p.id = %s AND k.id = %s;")

        self.sql_insert_product: str = "INSERT INTO product (product_url) VALUES(%s);"
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

    def create_user_product(
        self,
        user_id: int,
        request: ProductKeywordRequest
    ) -> UserProductKeywordResponse | None:

        self.cursor.execute("SELECT COUNT(*) FROM user_product_keyword WHERE user_id = %s;", (user_id,))
        count: int = self.cursor.fetchone()[0]

        if count <= 10:
            self.cursor.execute(self.sql_check_product, (request.product_url,))
            product_raw: tuple = self.cursor.fetchone()
            if not product_raw:
                self.cursor.execute(self.sql_insert_product, (request.product_url,))
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
                id=keyword_id,
                keyword=request.keyword
            )

            product_response: ProductResponse = ProductResponse(
                id=product_id,
                product_url=request.product_url,
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

        self.cursor.execute(self.sql_check_product, (request.product_url,))
        product_raw: tuple = self.cursor.fetchone()

        if not product_raw:
            self.cursor.execute(self.sql_insert_product, (request.product_url,))
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
            id=product_id,
            product_url=request.product_url
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
                id=user_product_keyword_id,
                product_url=f"{user_product_keyword_id}"
            )

        return user_delete_result
