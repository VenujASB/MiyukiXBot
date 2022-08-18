from dotenv import load_dotenv
from os import environ

load_dotenv("config.env")

BOT_TOKEN = environ.get("BOT_TOKEN", "")
API_ID = int(environ.get("API_ID", 18862638))
API_HASH = environ.get("API_HASH", "2a4a8dc0c1f6c9cb65f9f144439558ae")
API_ID1 = int(environ.get("API_ID1", 18862638))
API_HASH1 = environ.get("API_HASH1", "2a4a8dc0c1f6c9cb65f9f144439558ae")
SUDO_USERS_ID = [int(x) for x in environ.get("SUDO_USERS_ID", "1984415770").split()]
LOG_GROUP_ID = int(environ.get("LOG_GROUP_ID", "-1001760327326"))
BASE_DB = environ.get("BASE_DB", "mongodb+srv://base:base@cluster0.sgvgi.mongodb.net/?retryWrites=true&w=majority")
MONGO_URL = environ.get("MONGO_URL", "mongodb+srv://mongo:mongo@cluster0.lyjqq.mongodb.net/?retryWrites=true&w=majority")
ARQ_API_URL = environ.get("ARQ_API_URL", None)
ARQ_API_KEY = environ.get("ARQ_API_KEY", "GCDDVZ-TZLNPQ-TPWZQZ-JYGDBV-ARQ")
COMMAND_PREFIXES = environ.get("COMMAND_PREFIXES", "/")



