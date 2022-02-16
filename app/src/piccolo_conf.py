from environs import Env
from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

env = Env()
env.read_env()

config_db = {
    "host": env.str("POSTGRES_HOST"),
    "port": env.int("POSTGRES_PORT"),
    "database": env.str("POSTGRES_DATABASE_NAME"),
    "user": env.str("POSTGRES_USER"),
    "password": env.str("POSTGRES_PASSWORD"),
}

DB = PostgresEngine(config_db, log_queries=True)


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["transfer.piccolo_app"])
