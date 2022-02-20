from datetime import date
from pydantic import BaseModel, EmailStr, conint, constr
from transfer.tables import Customer

class UserModel(BaseModel):
    name: constr(max_length=100)
    surname: constr(max_length=100)
    email: EmailStr
    patronomic: constr(max_length=100) | None
    date_of_birth: date | None
    role: conint(ge=1, le=3) = 1
    document_name: constr(max_length=50) | None
    document_ident_1: constr(max_length=50) | None
    document_ident_2: constr(max_length=50) | None

    def save(self):
        Customer.insert(
            name=self.name,
            surname=self.surname,
            email=self.email,
            patronomic=self.patronomic,
            date_of_birth=self.date_of_birth,
            document_name=self.document_name,
            document_ident_1=self.document_ident_1,
            document_ident_2=self.document_ident_2,
            role = self.role
        ).run_sync()

