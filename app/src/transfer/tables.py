from piccolo.columns.column_types import Date, ForeignKey, Numeric, Varchar
from piccolo.table import Table


class Role(Table):
    """
    describes possible roles in the system (as castomer/operator/administrator)
    """

    name = Varchar(length=20)


class Customer(Table):
    """
    describes all users in the system - customer, operator and administrator
    """

    name = Varchar(length=100)
    surname = Varchar(length=100)
    patronomic = Varchar(length=100, null=True)
    date_of_birth = Date(null=True)
    role = ForeignKey(references=Role)
    document_name = Varchar(length=50)
    document_ident_1 = Varchar(length=50)
    document_ident_2 = Varchar(length=50)
    email = Varchar(length=255)


class Currency(Table):  #
    """
    this class describe k#ind of currency (ISO code), with may be in the system,
    according with https:#//en.wikipedia.org/wiki/List_of_circulating_currencies
    """

    name = Varchar(length=3)


class Account(Table):
    """
    the account number is bound to the user and currency. But the one used for money
    transfers is the user id - then the account is multi-currency
    when storing the amount of money in the account, the decimal data type is used
    """

    currency = ForeignKey(references=Currency)
    user = ForeignKey(references=Customer)
    amount = Numeric()  # return Decimal type
