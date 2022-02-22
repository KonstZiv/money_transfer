
from fastapi import FastAPI
from piccolo.utils.pydantic import create_pydantic_model
from . import constants
from transfer import tables
from . import models


app = FastAPI()

CustomerModelDB = create_pydantic_model(tables.Customer)

@app.post('/users/', response_model=models.Customer, tags=['user'])
async def create_user(user: models.Customer) -> tables.Customer:
    """
    Operation: creating a new user
    Input: models.Customer, 
        required filds: name, surname, email 
        optional filds: patronomic, document_name,
            document_ident_1, document_ident_2, date_of_birth
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


@app.put('/users/', response_model=models.CustomerUpdate, tags=['user'])
async def update_user(user: models.CustomerUpdate, tags=['user']) -> tables.Customer:
    """
    Operation: updating an existing user
    Input: models.CustomerUpdate, 
        required filds: id, name, surname, email, 
            document_name, document_ident_1, 
            date_of_birth
        optional fild: patronomic, document_ident_2
        the value of the role field will be ignored and 
            automatically assigned Role.CUSTOMER
    Returns: update user
    Access: available for operator and administrator
    Business logic: for any face-to-face operation, the operator 
    is obliged to verify the user according to the relevant documents 
    and update the information in the database
    Additionally: verification information is entered into the database
    """
    pass


