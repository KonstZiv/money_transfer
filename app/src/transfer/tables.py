#from piccolo.columns.column_types import Date, ForeignKey, Varchar
#from piccolo.table import Table
#
#
#class Role(Table):
#    """
#    describes possible roles in the system (as castomer/operator/administrator)
#    """
#
#    name = Varchar(length=20)
#
#
#class User(Table):
#    """
#    describes all users in the system - customer, operator and administrator
#    """
#
#    name = Varchar(length=100)
#    surname = Varchar(length=100)
#    patronomic = Varchar(length=100, null=True)
#    date_of_birth = Date(null=True)
#    role = ForeignKey(references=Role)
#    document_name = Varchar(length=50)
#    document_ident_1 = Varchar(length=50)
#    document_ident_2 = Varchar(length=50)
#    email = Varchar(length=255)
#
#class Currency(Table):#
#    """#
#    this class describe k#ind of currency (ISO code), with may be in the system,
#    according with https:#//en.wikipedia.org/wiki/List_of_circulating_currencies
#    """#
#    name = Varchar(length#=3)


