from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import INTEGER

from src.core.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER(unsigned=True), primary_key=True)
    email = Column(String(320), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    @staticmethod
    def hash_password(password):
        return sha256.hash(password)

    def verify_password(
        self,
        password,
    ):
        return sha256.verify(password, self.password)
