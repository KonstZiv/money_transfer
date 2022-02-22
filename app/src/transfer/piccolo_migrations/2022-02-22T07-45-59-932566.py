from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Date
from piccolo.columns.defaults.date import DateNow


ID = "2022-02-22T07:45:59:932566"
VERSION = "0.69.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="transfer", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Customer",
        tablename="customer",
        column_name="date_of_birth",
        params={"default": None},
        old_params={"default": DateNow()},
        column_class=Date,
        old_column_class=Date,
    )

    return manager
