import os

from pony import orm
import blogsley.config
from blogsley.config import config

db = orm.Database()
blogsley.config.db = db
'''
def load_db():
    filename = config('DATABASE_URL')
    print(filename)
    db.bind(provider='sqlite', filename=filename, create_db=True)
    db.generate_mapping(create_tables=True)
    return db
'''
def load_db():
    db.bind(provider='postgres',
        user=os.environ.get("POSTGRES_USER", ""),
        password=os.environ.get("POSTGRES_PASSWORD", ""),
        host=os.environ.get("POSTGRES_HOST", ""),
        database=os.environ.get("POSTGRES_DB", "")
    )

    db.generate_mapping(create_tables=True)
    return db
