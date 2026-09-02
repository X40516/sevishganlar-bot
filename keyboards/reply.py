"""
Doimiy (Reply) klaviaturalar.
"""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

MAIN_MENU_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💑 Juftimni ulash"), KeyboardButton(text="❤️ Juftim")],
        [KeyboardButton(text="💌 Xat yuborish"), KeyboardButton(text="🎲 Juftlik o'yinlari")],
        [KeyboardButton(text="💭 Bugungi savol"), KeyboardButton(text="🎁 Virtual sovg'alar")],
        [KeyboardButton(text="📸 Xotiralar"), KeyboardButton(text="❤️ Birga bo'lgan kunlar")],
        [KeyboardButton(text="🔔 Bildirishnomalar"), KeyboardButton(text="⚙️ Sozlamalar")],
        [KeyboardButton(text="ℹ️ Yordam")],
    ],
    resize_keyboard=True,
)
