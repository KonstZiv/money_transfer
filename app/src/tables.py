from piccolo.table import Table
from piccolo.columns import ForeignKey, Integer, Varchar


class User(Table):
    name = Varchar(length=100)
    surname = Varchar(length=100)
    patronomic = Varchar(length=100, null=True)
    