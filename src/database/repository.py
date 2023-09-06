from src.database.connect import db


class UserRepository:
    def __init__(self):
        self.db = db
        self.cursor = db.cursor()

    def get_user_by_username(self, username: str) -> tuple:

        sql: str = "SELECT * FROM user WHERE username = %s;"
        self.cursor.execute(sql, (username,))
        user: tuple = self.cursor.fetchall()

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
