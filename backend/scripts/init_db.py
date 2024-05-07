import os

from app import models, config, crud
from app.dependencies import ContextManager, ADMIN_USER_SCHEMA
from app.database import engine

def reset_db():
    if (os.path.isfile(config.DATABASE_PATH)):
        print("Removing existing DB")
        os.remove(config.DATABASE_PATH)
    print("Creating new DB")
    models.Base.metadata.create_all(bind=engine)
    with ContextManager() as db:
        print("Adding admin user")
        crud.create_user(db, ADMIN_USER_SCHEMA)
    print("DB reset!")
    

if __name__ == "__main__":
    reset_db()

