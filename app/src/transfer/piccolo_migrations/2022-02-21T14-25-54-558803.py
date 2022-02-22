from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2022-02-21T14:25:54:558803"
VERSION = "0.69.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="transfer", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="document_name",
        params={"null": True},
        old_params={"null": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="document_ident_1",
        params={"null": True},
        old_params={"null": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="document_ident_2",
        params={"null": True},
        old_params={"null": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    return manager
