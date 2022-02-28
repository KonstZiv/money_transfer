from fastapi import FastAPI
from transfer import tables

from . import constants, models

app = FastAPI()


@app.post("/users/", response_model=models.Customer, tags=["user"])
async def create_user(user: models.Customer) -> tables.Customer:
    """
    Operation: creating a new user
    Input: models.Customer,
        required filds: firstname, lastname, email
        optional filds: document_name, document_ident_1,
            document_ident_2, date_of_birth
        the value of the role field will be ignored and
            automatically assigned Role.CUSTOMER
    Returns: new user
    Access: available for operator and administrator
    Business logic: used when creating a new user
    """

    user.role = constants.Role.CUSTOMER
    user_dict = user.dict()
    new_customer = tables.Customer(**user_dict)
    await new_customer.save()
    return new_customer


@app.put("/users/", response_model=models.Customer, tags=["user"])
async def update_user(user: models.CustomerUpdate):
    """
    Operation: updating an existing user
    Input: models.CustomerUpdate,
        required filds: id, name, surname, email,
            document_name, document_ident_1,
            date_of_birth
        optional fild: document_ident_2
        the value of the role field will be ignored and
            automatically assigned Role.CUSTOMER
    Returns: update user
    Access: available for operator and administrator
    Business logic: for any face-to-face operation, the operator
    is obliged to verify the user according to the relevant documents
    and update the information in the database
    TODO!!!: Additionally: verification information is entered into
    the database
    """
    # TODO - a record of the ID of the person who made the change (or checked
    # if there was no change) and the time of the event
    print(f"user: {user}")
    await tables.Customer.update(
        {
            tables.Customer.firstname: user.firstname,
            tables.Customer.lastname: user.lastname,
            tables.Customer.date_of_birth: user.date_of_birth,
            tables.Customer.role: constants.Role.CUSTOMER,
            tables.Customer.document_name: user.document_name,
            tables.Customer.document_ident_1: user.document_ident_1,
            tables.Customer.document_ident_2: (
                user.document_ident_2 if user.document_ident_2 else None
            ),
            tables.Customer.email: user.email,
        }
    ).where(tables.Customer.id == user.id)

    return await tables.Customer.objects().get(tables.Customer.id == user.id)
