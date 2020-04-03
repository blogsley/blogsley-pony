from pony import orm
import blogsley.config
from blogsley.config import config

db = orm.Database()
blogsley.config.db = db

def load_db():
    filename = config.DATABASE_URI
    print(filename)
    db.bind(provider='sqlite', filename=filename, create_db=True)
    db.generate_mapping(create_tables=True)
    return db