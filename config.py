"""
Konfiguratsiya: .env fayldan sozlamalarni o'qiydi.
"""
import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

_admin_id_raw = os.getenv("ADMIN_ID", "")
try:
    ADMIN_ID = int(_admin_id_raw)
except (TypeError, ValueError):
    ADMIN_ID = None

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. .env faylini tekshiring.")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL topilmadi. .env faylini tekshiring.")

# asyncpg drayveri uchun URL formatini moslashtirish (Railway/Render odatda
# postgres:// yoki postgresql:// formatida beradi).
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

DAILY_QUESTION_HOUR = int(os.getenv("DAILY_QUESTION_HOUR", "10"))
DAILY_MESSAGE_HOUR = int(os.getenv("DAILY_MESSAGE_HOUR", "19"))
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
