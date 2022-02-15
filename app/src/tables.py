from piccolo.columns import Date, ForeignKey, Varchar
from piccolo.table import Table


class Role(Table):
    """
    describes possible roles in the system (as castomer/operator/administrator)
    """

    name = Varchar(length=20)


class User(Table):
    """
    describes all users in the system - customer, operator and administrator
    """

    name = Varchar(length=100)
    surname = Varchar(length=100)
    patronomic = Varchar(length=100, null=True)
    date_of_birth = Date()
    role = ForeignKey(references=Role)
    document_name = Varchar(length=50)
    document_ident_1 = Varchar(length=50)
    document_ident_2 = Varchar(length=50)


class Channel(Table):
    """
    describes all communication channels that are allowed to be used
    """

    name = Varchar(length=50)


class Contact(Table):
    """
    describes each identifier for communication with binding to the
    user and communication channel
    """

    id_user = ForeignKey(references=User)
    id_channel = ForeignKey(references=Channel)
    ident = Varchar(length=255)
