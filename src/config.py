from dotenv import load_dotenv

from src.services.env_utils import get_env_var, get_sequence_from_env

load_dotenv(override=True)

# --- Core Configuration ---
MODE = get_env_var("MODE", default="PROD", raise_exc=True)
DATABASE_URL = get_env_var("DB_URL", raise_exc=True)
BOT_TOKEN = get_env_var("BOT_TOKEN", raise_exc=True)

# --- Access Control ---
ADMIN_USERS = get_sequence_from_env("TELEGRAM_ADMINS")
ALLOWED_CHAT_IDS = get_sequence_from_env("ALLOWED_CHAT_IDS")

# --- Redis Configration ---
REDIS_URL = get_env_var("REDIS_URL", raise_exc=True)
