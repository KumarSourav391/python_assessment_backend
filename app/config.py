import os
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname

load_dotenv(find_dotenv())

def get_envfile(ENV=os.getenv("ENV")):
    if ENV=="Production":
        return ".env.production"
    if ENV == "development":
        return ".env.development"
    if ENV == "test":
        return ".env.test"
    else:
        print("Please set a Env")
        return ""

env_file = get_envfile()
env_file_path = join(dirname(__file__),env_file)
load_dotenv(env_file_path,override=True)

SQLALCHEMY_DATABASE_URI = (
    "postgresql://"
    + os.environ.get("DB_USERNAME", "")
    + ":"
    + os.environ.get("DB_PASSWORD", "")
    + "@"
    + os.environ.get("DB_HOSTNAME", "")
    + ":"
    + os.environ.get("DB_PORT", "")
    + "/"
    + os.environ.get("DATABASE", "")
)






