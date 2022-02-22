from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar


ID = "2022-02-22T08:26:44:452426"
VERSION = "0.69.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="transfer", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="email",
        params={"index": True},
        old_params={"index": False},
        column_class=Varchar,
        old_column_class=Varchar,
    )

    return manager
