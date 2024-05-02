# secret key used for encoding session data
# should be in some .env file in production, not committed
# but this works for now
# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = "6d7b5968fccbc2b4d484280030d9424536091a64a9bd7c167e91ea18aaa98312"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_PATH = "./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

CURR_PLAN = 1
