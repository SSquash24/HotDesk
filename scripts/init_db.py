import os

from app import models, config, crud
from app.dependencies import ContextManager, ADMIN_USER_SCHEMA
from app.database import engine



if __name__ == "__main__":
    if (os.path.isfile(config.DATABASE_PATH)):
        os.remove(config.DATABASE_PATH)

    models.Base.metadata.create_all(bind=engine)
    with ContextManager() as db:
        crud.create_user(db, ADMIN_USER_SCHEMA)

