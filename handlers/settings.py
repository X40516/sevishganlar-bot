"""
⚙️ Sozlamalar bo'limi.
"""
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import get_couple_for_user, get_notification_settings, get_partner_user, toggle_notification
from utils.helpers import days_together_breakdown, home_button

router = Router(name="settings")

NOTIF_LABELS = {
    "daily_question": "💭 Bugungi savol",
    "daily_message": "❤️ Kunlik romantik xabar",
    "new_letter": "💌 Yangi xat",
    "gift": "🎁 Sovg'a",
    "special_date": "📅 Maxsus sana",
}


def _settings_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="settings:notif")],
            [InlineKeyboardButton(text="🌐 Til", callback_data="settings:lang")],
            [InlineKeyboardButton(text="👤 Profil", callback_data="settings:profile")],
            [InlineKeyboardButton(text="❤️ Juftlik sozlamalari", callback_data="settings:couple")],
            [InlineKeyboardButton(text="ℹ️ Bot haqida", callback_data="settings:about")],
            [home_button()],
        ]
    )


@router.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: Message) -> None:
    await message.answer("⚙️ Sozlamalar:", reply_markup=_settings_menu_kb())


async def _notif_kb(session: AsyncSession, user_id: int) -> InlineKeyboardMarkup:
    settings = await get_notification_settings(session, user_id)
    buttons = []
    for field, label in NOTIF_LABELS.items():
        status = "✅" if getattr(settings, field) else "❌"
        buttons.append([InlineKeyboardButton(text=f"{status} {label}", callback_data=f"settings:notif_toggle:{field}")])
    buttons.append([home_button()])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text == "🔔 Bildirishnomalar")
async def notif_menu_from_main(message: Message, session: AsyncSession, db_user: User) -> None:
    kb = await _notif_kb(session, db_user.id)
    await message.answer("🔔 Bildirishnomalar (yoqish/o'chirish uchun bosing):", reply_markup=kb)


@router.callback_query(F.data == "settings:notif")
async def settings_notif(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    kb = await _notif_kb(session, db_user.id)
    await callback.message.edit_text("🔔 Bildirishnomalar (yoqish/o'chirish uchun bosing):", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("settings:notif_toggle:"))
async def settings_notif_toggle(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    field = callback.data.split(":")[2]
    await toggle_notification(session, db_user.id, field)
    kb = await _notif_kb(session, db_user.id)
    await callback.message.edit_text("🔔 Bildirishnomalar (yoqish/o'chirish uchun bosing):", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "settings:lang")
async def settings_lang(callback: CallbackQuery, db_user: User) -> None:
    await callback.message.edit_text("🌐 Hozirgi til: 🇺🇿 O'zbekcha")
    await callback.answer()


@router.callback_query(F.data == "settings:profile")
async def settings_profile(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    couple_status = "❤️ Ulangan" if couple else "❌ Ulanmagan"
    sana = couple.anniversary_date.strftime("%d.%m.%Y") if couple and couple.anniversary_date else "belgilanmagan"
    username = f"@{db_user.username}" if db_user.username else "yo'q"
    await callback.message.edit_text(
        f"👤 Ism: {db_user.full_name}\n"
        f"🆔 Username: {username}\n"
        f"❤️ Juftlik holati: {couple_status}\n"
        f"📅 Juftlik sanasi: {sana}"
    )
    await callback.answer()


@router.callback_query(F.data == "settings:couple")
async def settings_couple(callback: CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Sana", callback_data="days:set")],
            [InlineKeyboardButton(text="💑 Juftim", callback_data="goto:memories")],
            [InlineKeyboardButton(text="💔 Juftlikni ajratish", callback_data="couple:unpair_confirm")],
        ]
    )
    await callback.message.edit_text("❤️ Juftlik sozlamalari:", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "settings:about")
async def settings_about(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "ℹ️ @JuftimBotbot — sevishgan juftliklar uchun maxsus bot.\n\n"
        "Xatlar, o'yinlar, kunlik savollar, sovg'alar va xotiralar orqali "
        "munosabatlaringizni yanada mustahkamlang. 💕"
    )
    await callback.answer()
