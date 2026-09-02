"""
Umumiy yordamchi funksiyalar.
"""
from datetime import date

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message


def days_together_breakdown(anniversary: date, today: date | None = None) -> tuple[int, int, int, int]:
    """(jami_kun, yil, oy, kun) qaytaradi."""
    today = today or date.today()
    total_days = (today - anniversary).days

    years = today.year - anniversary.year
    months = today.month - anniversary.month
    days = today.day - anniversary.day

    if days < 0:
        months -= 1
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        import calendar

        days += calendar.monthrange(prev_year, prev_month)[1]
    if months < 0:
        years -= 1
        months += 12

    return total_days, years, months, days


def back_button(callback_data: str, text: str = "⬅️ Orqaga") -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback_data)


def home_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="menu:home")


async def safe_edit(target: Message | CallbackQuery, text: str, reply_markup=None) -> None:
    message = target.message if isinstance(target, CallbackQuery) else target
    try:
        await message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest as exc:
        if "message is not modified" not in str(exc):
            await message.answer(text, reply_markup=reply_markup)
