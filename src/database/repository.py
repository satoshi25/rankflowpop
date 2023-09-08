from typing import List

from src.database.connect import db
from src.schema.request import ProductRequest
from src.schema.response import ProductResponse, KeywordResponse


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

    def create_user_product(
        self,
        user_id: int,
        request: ProductRequest
    ) -> ProductResponse:

        sql_check_product: str = "SELECT id FROM product WHERE product_url = %s;"
        sql_insert_product: str = "INSERT INTO product (product_url) VALUES(%s);"

        sql_check_keyword: str = "SELECT id FROM keyword WHERE keyword = %s;"
        sql_insert_keyword: str = "INSERT INTO keyword (keyword) VALUES(%s);"

        sql_check_product_keyword: str = \
            ("SELECT pk.id "
             "FROM product_keyword pk "
             "JOIN keyword k ON pk.keyword_id = k.id "
             "JOIN product p ON pk.product_id = p.id "
             "WHERE k.keyword = %s AND p.product_url = %s;")

        sql_insert_product_keyword: str = \
            "INSERT INTO product_keyword (product_id, keyword_id) VALUES(%s, %s);"

        sql_check_user_product_keyword: str = \
            ("SELECT upk.id "
             "FROM user_product_keyword upk "
             "JOIN user u ON upk.user_id = u.id "
             "JOIN product_keyword pk ON upk.product_keyword_id = pk.id "
             "JOIN keyword k ON pk.keyword_id = k.id "
             "JOIN product p ON pk.product_id = p.id "
             "WHERE u.id = %s AND p.product_url = %s AND k.keyword = %s;")

        sql_insert_user_product_keyword: str = \
            "INSERT INTO user_product_keyword (user_id, product_keyword_id) VALUES (%s, %s);"

        self.cursor.execute(sql_check_product, (request.product_url,))
        product_raw: tuple = self.cursor.fetchone()
        if not product_raw:
            self.cursor.execute(sql_insert_product, (request.product_url,))
            self.db.commit()
            product_id: int = self.cursor.lastrowid
        else:
            product_id: int = product_raw[0]
        request_keywords: List[KeywordResponse] = []

        for keyword in request.keywords:
            self.cursor.execute(sql_check_keyword, (keyword.keyword,))
            keyword_raw: tuple = self.cursor.fetchone()
            if not keyword_raw:
                self.cursor.execute(sql_insert_keyword, (keyword.keyword,))
                self.db.commit()
                keyword_id: int = self.cursor.lastrowid
            else:
                keyword_id: int = keyword_raw[0]

            self.cursor.execute(sql_check_product_keyword, (product_id, keyword_id,))
            product_keyword_raw: tuple = self.cursor.fetchone()
            if not product_keyword_raw:
                self.cursor.execute(sql_insert_product_keyword, (product_id, keyword_id,))
                self.db.commit()
                product_keyword_id: int = self.cursor.lastrowid
            else:
                product_keyword_id: int = product_keyword_raw[0]

            self.cursor.execute(sql_check_user_product_keyword, (user_id, product_id, keyword_id))
            user_product_keyword_raw: tuple = self.cursor.fetchone()
            if not user_product_keyword_raw:
                self.cursor.execute(sql_insert_user_product_keyword, (user_id, product_keyword_id,))
                self.db.commit()

            request_keywords.append(KeywordResponse(id=keyword_id, keyword=keyword.keyword))
        product: ProductResponse = ProductResponse(id=product_id, product_url=request.product_url, keywords=request_keywords)

        return product
