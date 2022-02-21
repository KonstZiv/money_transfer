from fastapi import FastAPI
from app.models import UserModel

app = FastAPI()

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "This is root page"}

@app.get('/user/{email_str}', tags=['user'])
async def read_user(email_str) -> dict:
    """
    возвращает все данные по пользователю, включая состояние его счета
    доступ: для пользователей автоизованных с ролью admin и operator - неограниченный
    доступ: для авторизованного пользователя с ролью customer - только к своим данным
    """
    return {
        'message': f'data for user: {email_str}'
    }

@app.post("/create_user/")
async def create_user():
    """
    получив запрос создать в БД новго пользователя
    """
    pass

