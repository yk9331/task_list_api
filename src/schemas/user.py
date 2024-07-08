from pydantic import EmailStr, Field, SecretStr, field_serializer

from src.schemas.base_model import CamelModel


class UserCreate(CamelModel):
    email: EmailStr
    password: SecretStr

    @field_serializer("password", when_used="json")
    def serialize_password(password: SecretStr):
        return password.get_secret_value()


class UserUpdate(CamelModel):
    pass


class UserRegister(UserCreate):
    password: SecretStr = Field(min_length=8)


class UserLogin(UserCreate):
    password: SecretStr = Field(min_length=8)


class UserToken(CamelModel):
    access_token: str
    token_type: str = "bearer"
