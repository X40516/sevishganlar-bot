"""
⚙️ Sozlamalar bo'limi.
"""
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import get_couple_for_user, get_notification_settings, set_user_language, toggle_notification
from keyboards.reply import MENU_TEXTS, get_main_menu
from locales.texts import LANGUAGES, t
from utils.helpers import home_button

router = Router(name="settings")

NOTIF_LABEL_KEYS = {
    "daily_question": "notif_daily_question",
    "daily_message": "notif_daily_message",
    "new_letter": "notif_new_letter",
    "gift": "notif_gift",
    "special_date": "notif_special_date",
}


def _settings_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "settings_notif_btn"), callback_data="settings:notif")],
            [InlineKeyboardButton(text=t(lang, "settings_lang_btn"), callback_data="settings:lang")],
            [InlineKeyboardButton(text=t(lang, "settings_profile_btn"), callback_data="settings:profile")],
            [InlineKeyboardButton(text=t(lang, "settings_couple_btn"), callback_data="settings:couple")],
            [InlineKeyboardButton(text=t(lang, "settings_about_btn"), callback_data="settings:about")],
            [home_button(lang)],
        ]
    )


@router.message(F.text.in_(MENU_TEXTS["menu_settings"]))
async def settings_menu(message: Message, db_user: User) -> None:
    await message.answer(t(db_user.language, "settings_prompt"), reply_markup=_settings_menu_kb(db_user.language))


async def _notif_kb(session: AsyncSession, user_id: int, lang: str) -> InlineKeyboardMarkup:
    settings = await get_notification_settings(session, user_id)
    buttons = []
    for field, label_key in NOTIF_LABEL_KEYS.items():
        status = "✅" if getattr(settings, field) else "❌"
        buttons.append([InlineKeyboardButton(text=f"{status} {t(lang, label_key)}", callback_data=f"settings:notif_toggle:{field}")])
    buttons.append([home_button(lang)])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(F.text.in_(MENU_TEXTS["menu_notif"]))
async def notif_menu_from_main(message: Message, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    kb = await _notif_kb(session, db_user.id, lang)
    await message.answer(t(lang, "notif_prompt"), reply_markup=kb)


@router.callback_query(F.data == "settings:notif")
async def settings_notif(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    kb = await _notif_kb(session, db_user.id, lang)
    await callback.message.edit_text(t(lang, "notif_prompt"), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data.startswith("settings:notif_toggle:"))
async def settings_notif_toggle(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    field = callback.data.split(":")[2]
    await toggle_notification(session, db_user.id, field)
    kb = await _notif_kb(session, db_user.id, lang)
    await callback.message.edit_text(t(lang, "notif_prompt"), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "settings:lang")
async def settings_lang(callback: CallbackQuery, db_user: User) -> None:
    lang = db_user.language
    buttons = [[InlineKeyboardButton(text=name, callback_data=f"settings:lang_set:{code}")] for code, name in LANGUAGES.items()]
    buttons.append([home_button(lang)])
    await callback.message.edit_text(t(lang, "lang_prompt"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer()


@router.callback_query(F.data.startswith("settings:lang_set:"))
async def settings_lang_set(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    new_lang = callback.data.split(":")[2]
    await set_user_language(session, db_user.id, new_lang)
    await callback.message.edit_text(t(new_lang, "lang_changed"))
    await callback.message.answer(t(new_lang, "home_menu"), reply_markup=get_main_menu(new_lang))
    await callback.answer()


@router.callback_query(F.data == "settings:profile")
async def settings_profile(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    status = t(lang, "profile_paired") if couple else t(lang, "profile_not_paired")
    sana = couple.anniversary_date.strftime("%d.%m.%Y") if couple and couple.anniversary_date else t(lang, "profile_no_date")
    username = f"@{db_user.username}" if db_user.username else "-"
    await callback.message.edit_text(
        t(lang, "profile_text", name=db_user.full_name, username=username, status=status, date=sana)
    )
    await callback.answer()


@router.callback_query(F.data == "settings:couple")
async def settings_couple(callback: CallbackQuery, db_user: User) -> None:
    lang = db_user.language
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "couple_set_date_btn"), callback_data="days:set")],
            [InlineKeyboardButton(text=t(lang, "couple_unpair_btn"), callback_data="couple:unpair_confirm")],
            [home_button(lang)],
        ]
    )
    await callback.message.edit_text(t(lang, "settings_couple_btn"), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "settings:about")
async def settings_about(callback: CallbackQuery, db_user: User) -> None:
    await callback.message.edit_text(t(db_user.language, "about_text"))
    await callback.answer()
