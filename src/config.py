from dotenv import load_dotenv

from src.services.env_utils import get_env_var, get_sequence_from_env

load_dotenv(override=True)

# --- Core Configuration ---
MODE = get_env_var("MODE", default="PROD", raise_exc=True)
BOT_TOKEN = get_env_var("BOT_TOKEN", raise_exc=True)

# --- Access Control ---
ADMIN_USERS = get_sequence_from_env("TELEGRAM_ADMINS")
ALLOWED_CHAT_IDS = get_sequence_from_env("ALLOWED_CHAT_IDS")

# --- MySQL Configuration ---

MYSQL_DATABASE = get_env_var("MYSQL_DATABASE")
MYSQL_USER = get_env_var("MYSQL_USER")
MYSQL_PASSWORD = get_env_var("MYSQL_PASSWORD")
MYSQL_PORT = get_env_var("MYSQL_PORT")
MYSQL_HOST = get_env_var("MYSQL_HOST")


# --- Redis Configration ---
REDIS_URL = get_env_var("REDIS_URL", raise_exc=True)
