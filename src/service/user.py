import bcrypt

from src.schema.response import UserResponse
from src.database.repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.encode: str = "UTF-8"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(password.encode(self.encode), bcrypt.gensalt())
        return hashed_password.decode(self.encode)

    def create_user(self, username: str, password: str) -> UserResponse | None:
        hashed_password = self.hash_password(password=password)
        user: tuple = self.user_repo.get_user_by_username(username=username)

        if not user:
            return None

        raw_data: tuple = self.user_repo.create_user(username=username, password=hashed_password)

        user: UserResponse = UserResponse(
            id=raw_data[0],
            username=raw_data[1]
        )

        return user
