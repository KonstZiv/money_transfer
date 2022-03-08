from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from environs import Env
from pydantic import EmailStr, PastDate
from app.constants import Role

from app.models import CustomerInDB, CustomerUpdate, StrDocument, StrName
from transfer import tables

env = Env()
env.read_env()

JWT_SECRET = env.str("JWT_SECRET")
JWT_ALGORITM = env.str("JWT_ALGORITM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_customer(customer_email: str) -> CustomerInDB:
    """
    returns all data of the user with the given email
    (the email is unique for users in the database) 
    """
    customer = await tables.Customer.objects().get(
                    tables.Customer.email == customer_email
                                                )
    return customer


def authenticate_user(customer_email: str, password: str):
    pass


def fake_decode_token(token):
    """
    имитирует получение токена, его расшифровку, сопоставление с БД
    соотвествия токена и пользователя и возвращает пользователя,
    соотвествующего этому токену
    """
    return CustomerUpdate(
            id=1,
            firstname=token + 'fakedecoded',
            lastname=StrName('fakedecoded'),
            account_id=UUID('3fa85f64-5717-4562-b3fc-2c963f66afa6'),
            date_of_birth=PastDate(year=1985, month=3, day=2),
            role=Role.OPERATOR,
            document_ident_1=StrDocument('fakedecoded'),
            document_name=StrDocument('fakedecoded'),
            email=EmailStr('example@example.ua'),
                )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    имитирует получение текущего пользователя по декодированному токену
    через функцию fake_decode_token в случае если токен есть проходит
    декодирование
    """
    user = fake_decode_token(token)
    return user
