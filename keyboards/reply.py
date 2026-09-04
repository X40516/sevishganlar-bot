"""
Doimiy (Reply) klaviaturalar - ko'p tillilikni qo'llab-quvvatlaydi.
"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from locales.texts import LANGUAGES, t

MENU_KEYS = [
    "menu_pair", "menu_couple", "menu_letter", "menu_games", "menu_question",
    "menu_gift", "menu_memories", "menu_days", "menu_notif", "menu_settings", "menu_help",
]

MENU_TEXTS: dict[str, set[str]] = {
    key: {t(lang, key) for lang in LANGUAGES} for key in MENU_KEYS
}


def get_main_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "menu_pair")), KeyboardButton(text=t(lang, "menu_couple"))],
            [KeyboardButton(text=t(lang, "menu_letter")), KeyboardButton(text=t(lang, "menu_games"))],
            [KeyboardButton(text=t(lang, "menu_question")), KeyboardButton(text=t(lang, "menu_gift"))],
            [KeyboardButton(text=t(lang, "menu_memories")), KeyboardButton(text=t(lang, "menu_days"))],
            [KeyboardButton(text=t(lang, "menu_notif")), KeyboardButton(text=t(lang, "menu_settings"))],
            [KeyboardButton(text=t(lang, "menu_help"))],
        ],
        resize_keyboard=True,
    )
