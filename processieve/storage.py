from . import neoDriver
from .utils import list_models


def create_id_constraints():
    for model in list_models():
        neoDriver.execute_query(
            f"CREATE CONSTRAINT unique_{model.__name__.lower()}_id IF NOT EXISTS FOR (n:{model.__name__}) REQUIRE n.id IS UNIQUE;"
        )


def clear_database():
    neoDriver.execute_query("MATCH (n) DETACH DELETE n")
