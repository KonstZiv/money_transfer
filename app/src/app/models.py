import uuid
from typing import Optional

from app.constants import Role
from pydantic import (
                BaseModel, ConstrainedStr, EmailStr,
                Field, PastDate, validator
                )


class StrName(ConstrainedStr):
    """
    class provides validation of a string with a length of up to 100 characters
    """

    max_lenght = 100


class StrDocument(ConstrainedStr):
    """
    class provides validation of a string with a length of up to 50 characters
    """

    max_lenght = 50


class CustomerCreate(BaseModel):
    """
    the constraint model matches tables.Customer: required fields (firstname,
    lastname, email) optional fields (date_og_birth, role, document_name,
    document_ident_1, document_ident_2). Provides deeper type
    checking: pastedata, email
    """

    account_id: Optional[uuid.UUID] = None
    firstname: StrName
    lastname: StrName
    date_of_birth: Optional[PastDate] = None
    role: Optional[Role] = None
    document_name: Optional[StrDocument] = None
    document_ident_1: Optional[StrDocument] = None
    document_ident_2: Optional[StrDocument] = None
    email: EmailStr

    class Config:
        orm_mode = True

    @validator("account_id", pre=True, always=True)
    def set_account_id_if_none(cls, account_id):
        return account_id or uuid.uuid4()


class CustomerUpdate(CustomerCreate):
    """
    the model is used to validate data during user verification operations
    by the operator, the main difference from the Customer model is that
    all fields are required and the id field has been added
    """

    id: int
    account_id: uuid.UUID
    date_of_birth: PastDate
    role: Role = Role.CUSTOMER
    document_name: StrDocument
    document_ident_1: StrDocument
    document_ident_2: str = Field(None, max_length=50)

    class Config:
        orm_mode = True
