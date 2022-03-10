from datetime import timedelta

from app.auth.auth_handler import (
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_customer,
    create_access_token,
    get_current_user,
    only_admin_or_operator,
)
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from transfer import tables

from . import constants, models

app = FastAPI()


@app.post("/users/", response_model=models.CustomerCreate, tags=["user"])
async def create_user(
    user: models.CustomerCreate,
) -> tables.Customer:
    """
    Operation: creating a new user
    Input: models.CustomerCreate,
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


@app.put("/users/", response_model=models.CustomerCreate, tags=["user"])
async def update_user(
    user: models.CustomerUpdate,
    current_customer: models.CustomerInDB = Depends(only_admin_or_operator),
):
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


@app.get("/users/me", tags=["user"])
async def read_users_me(
    current_user: models.CustomerUpdate = Depends(get_current_user),
) -> models.CustomerUpdate:
    """
    test function - returns the current user
    """
    return current_user


@app.post("/token", response_model=models.Token, tags=["user"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """
    receives the authorization flow (login and password of the user) and
    returns a token if the login and password are correct
    """
    # username is his email
    customer = await authenticate_customer(form_data.username, form_data.password)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": customer.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}
