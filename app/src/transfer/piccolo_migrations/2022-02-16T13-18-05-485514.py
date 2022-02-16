from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2022-02-16T13:18:05:485514"
VERSION = "0.69.2"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
