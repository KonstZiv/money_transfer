from pydantic import BaseModel, Field, EmailStr, PastDate, ConstrainedStr
from app.constants import Role


class StrName(ConstrainedStr):
    max_lenght = 100

class StrDocum(ConstrainedStr):
    max_lenght = 50


class Customer(BaseModel):
    name: StrName
    surname: StrName
    patronomic: str = Field(None, max_length=100)
    date_of_birth: PastDate = Field(None)
    role: Role = Field(None)
    document_name: str = Field(None, max_length=50)
    document_ident_1: str = Field(None, max_length=50)
    document_ident_2: str = Field(None, max_length=50)
    email: EmailStr

    class Config:
        orm_mode=True


class CustomerUpdate(BaseModel):
    id: int
    name: StrName
    surname: StrName
    patronomic: str = Field(None, max_length=100)
    date_of_birth: PastDate
    role: Role = Role.CUSTOMER
    document_name: StrDocum
    document_ident_1: StrDocum
    document_ident_2: str = Field(None, max_length=50)
    email: EmailStr

    class Config:
        orm_mode=True










