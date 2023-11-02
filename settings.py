from envparse import Env

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://postgres:postgres@localhost:5433/edu_db",
)

APP_PORT = env.int("APP_PORT", default=8000)

SENTRY_URL = env.str(
    "SENTRY_URL",
    default="http://287c6bc942c24886aeaa238d3d208aae@localhost:9000/2",
)

SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

TEST_DATABASE_URL = env.str(
    "TEST_DATABASE_URL",
    default="postgresql+asyncpg://postgres_test:postgres_test@localhost:5434/edu_db_test",
)
