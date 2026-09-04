"""
❤️ Juftim bo'limi: ulanish, kod, ma'lumot, ajratish.
"""
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import create_pair_invite, deactivate_couple, get_couple_for_user, get_partner_user
from keyboards.reply import MENU_TEXTS, get_main_menu
from locales.texts import t
from utils.helpers import days_together_breakdown, home_button

router = Router(name="couple")


def _no_couple_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "couple_link_btn"), callback_data="couple:link")],
            [InlineKeyboardButton(text=t(lang, "couple_code_btn"), callback_data="couple:code")],
            [home_button(lang)],
        ]
    )


def _couple_info_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "couple_set_date_btn"), callback_data="days:set")],
            [InlineKeyboardButton(text=t(lang, "couple_send_letter_btn"), callback_data="goto:letters")],
            [InlineKeyboardButton(text=t(lang, "couple_memories_btn"), callback_data="goto:memories")],
            [InlineKeyboardButton(text=t(lang, "couple_unpair_btn"), callback_data="couple:unpair_confirm")],
            [home_button(lang)],
        ]
    )


async def show_couple_section(message: Message, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "couple_invite_prompt"), reply_markup=_no_couple_kb(lang))
        return

    partner = await get_partner_user(session, couple, db_user.id)
    if couple.anniversary_date:
        total_days, years, months, days = days_together_breakdown(couple.anniversary_date)
        sana_text = t(lang, "couple_date_set", date=couple.anniversary_date.strftime("%d.%m.%Y"), days=total_days)
    else:
        sana_text = t(lang, "couple_date_unset")

    await message.answer(
        t(lang, "couple_info", name=partner.full_name, sana=sana_text),
        reply_markup=_couple_info_kb(lang),
    )


@router.message(F.text.in_(MENU_TEXTS["menu_couple"] | MENU_TEXTS["menu_pair"]))
async def couple_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    await show_couple_section(message, session, db_user)


@router.callback_query(F.data == "couple:link")
async def couple_link(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    bot_info = await callback.bot.get_me()
    invite = await create_pair_invite(session, db_user.id)
    link = f"https://t.me/{bot_info.username}?start={invite.code}"
    await callback.message.answer(t(lang, "couple_link_sent", link=link))
    await callback.answer()


@router.callback_query(F.data == "couple:code")
async def couple_code(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    invite = await create_pair_invite(session, db_user.id)
    await callback.message.answer(t(lang, "couple_code_sent", code=invite.code))
    await callback.answer()


@router.callback_query(F.data == "couple:unpair_confirm")
async def couple_unpair_confirm(callback: CallbackQuery, db_user: User) -> None:
    lang = db_user.language
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "couple_unpair_yes"), callback_data="couple:unpair_yes"),
                InlineKeyboardButton(text=t(lang, "couple_unpair_no"), callback_data="couple:unpair_no"),
            ]
        ]
    )
    await callback.message.edit_text(t(lang, "couple_unpair_confirm"), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "couple:unpair_no")
async def couple_unpair_no(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await callback.message.delete()
    await show_couple_section(callback.message, session, db_user)
    await callback.answer()


@router.callback_query(F.data == "couple:unpair_yes")
async def couple_unpair_yes(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌", show_alert=True)
        return
    partner = await get_partner_user(session, couple, db_user.id)
    await deactivate_couple(session, couple.id)

    await callback.message.edit_text(t(lang, "couple_unpaired"))
    await callback.message.answer(t(lang, "couple_invite_prompt"), reply_markup=get_main_menu(lang))

    if partner:
        try:
            await callback.bot.send_message(
                partner.telegram_id,
                t(partner.language, "couple_partner_unpaired"),
                reply_markup=get_main_menu(partner.language),
            )
        except Exception:
            pass
    await callback.answer()
