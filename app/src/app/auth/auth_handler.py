from datetime import datetime, timedelta

from app.models import CustomerInDB, TokenData
from environs import Env
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from transfer import tables

env = Env()
env.read_env()

JWT_SECRET = env.str("JWT_SECRET")
JWT_ALGORITHM = env.str("JWT_ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = env.int("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    compares the received password (plain_password ) with the hashed
    password value stored in the database (hashed_password).
    Returns True on a match (when using the schema defined
    for the pvd_context instance) and False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    returns a hashed password for the 'password' argument,
    uses the bcrypt algorithm (module passlib)
    """
    return pwd_context.hash(password)


async def get_customer(customer_email: str) -> CustomerInDB | None:
    """
    returns all data of the user with the given email
    (the email is unique for users in the database)
    """
    customer = await tables.Customer.objects().get(
        tables.Customer.email == customer_email
    )
    if customer:
        return CustomerInDB(**customer.to_dict())


async def authenticate_customer(
    customer_email: str, password: str
) -> CustomerInDB | bool:
    """
    by login (email) and password returns all user data. In case of
    incorrect login (email) and/or password - returns False
    """
    customer = await get_customer(customer_email)
    if not customer or not verify_password(password, customer.hashed_password):
        return False
    return customer


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    creates a token with a lifetime of expires_delta (minutes).
    If expires_delta is not specified, the token lifetime is set to 15 minutes
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> CustomerInDB:
    """
    gets the current user by decoded token if the token passes decoding
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if not (customer_email := payload.get("sub")):
            raise credentials_exception
        token_data = TokenData(customer_email=customer_email)
    except JWTError:
        raise credentials_exception
    customer = await get_customer(customer_email=token_data.customer_email)
    if not customer:
        raise credentials_exception
    return customer
