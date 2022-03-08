from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from transfer import tables

from . import constants, models
from auth.auth_handler import get_current_user

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


@app.get("/users/me")
async def read_users_me(
    current_user: models.CustomerUpdate = Depends(get_current_user)
                    ) -> models.CustomerUpdate:
    return current_user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    при обращении к endpoint получает как данные формы (в соотвествии
    со спецификацией OAuth2):
    form_data.username: str (username OAuth2)
    form_data.password: str (password OAuth2)
    form_data.scopes: Optional(List[str]) = None (scope.split() - OAuth2)
    form_data.grant_type: Optional(str) = None (отличается от OAuth2)
    form_data.client_id: Optional(str) = None
    form_data.client_secret: Optional(str) = None

    далее обращается к БД по username/password и если такого клиента нет
    или пароль неверен райзит исключение
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = models.CustomerInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}