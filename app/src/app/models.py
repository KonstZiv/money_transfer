import uuid

from app.constants import Role
from passlib.context import CryptContext
from pydantic import BaseModel, ConstrainedStr, EmailStr, PastDate, validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

    account_id: uuid.UUID | None = None
    firstname: StrName
    lastname: StrName
    date_of_birth: PastDate | None = None
    role: Role | None = None
    document_name: StrDocument | None = None
    document_ident_1: StrDocument | None = None
    document_ident_2: StrDocument | None = None
    email: EmailStr

    class Config:
        orm_mode = True

    @validator("account_id", pre=True, always=True)
    def set_account_id_if_none(cls, account_id) -> uuid.UUID:
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
    document_ident_2: StrDocument | None = None

    class Config:
        orm_mode = True


class CustomerInDB(CustomerUpdate):
    """
    the model adds a field with the user's hashed password
    """

    hashed_password: str

    def verify(self, plain_password):
        """
        compares the received password (plain_password) with the hashed
        password value stored in the database (self.hashed_password).
        Returns True on a match (when using the schema defined
        for the pvd_context instance) and False otherwise.
        """
        return pwd_context.verify(plain_password, self.hashed_password)


class Token(BaseModel):
    """
    model for response when forming a token
    """

    access_token: str


class TokenData(BaseModel):
    """
    token payload model
    """

    customer_email: str | None = None
