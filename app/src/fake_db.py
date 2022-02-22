import asyncio

from faker import Faker
from datetime import date


from app.models import UserModel

async def fake_user(num: int) -> None:
    """
    add to DB num fake user
    """
    fake = Faker()
    today = date.today()
    date_start = today.replace(year=today.year - 80)
    date_finish = today.replace(year=today.year - 18)
    for _ in range(num):
        await UserModel(
            name=fake.first_name(),
            surname=fake.last_name(),
            date_of_birth= fake.date_between_dates(date_start, date_finish),
            email=fake.ascii_email()
        ).save()


if __name__ == '__main__':
    num = 10
    asyncio.run(fake_user((num)))
