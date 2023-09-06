from fastapi import Depends
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import os

from src.schema.response import UserResponse
from src.database.repository import UserRepository

load_dotenv()


class UserService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo
        self.encoding: str = os.getenv("HASHING_ENCODING")
        self.secret_key: str = os.getenv("JWT_SECRET_KEY")
        self.jwt_algorithm: str = os.getenv("JWT_ALGORITHM")

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(self.encoding), hashed_password.encode(self.encoding))

    def create_jwt(self, username: str) -> str:
        access_token: str = jwt.encode(
            {
                "sub": username,
                "exp": datetime.now() + timedelta(days=7)
            },
            key=self.secret_key,
            algorithm=self.jwt_algorithm
        )

        return access_token

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
