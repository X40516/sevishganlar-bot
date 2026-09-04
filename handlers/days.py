"""
❤️ Birga bo'lgan kunlar bo'limi.
"""
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import get_couple_for_user, get_partner_user, set_anniversary_date
from handlers.states import DaysStates
from keyboards.reply import MENU_TEXTS
from locales.texts import t
from utils.helpers import days_together_breakdown, home_button

router = Router(name="days")


@router.message(F.text.in_(MENU_TEXTS["menu_days"]))
async def days_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "no_couple"))
        return

    if couple.anniversary_date is None:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=t(lang, "days_set_btn"), callback_data="days:set")], [home_button(lang)]]
        )
        await message.answer(t(lang, "days_unset"), reply_markup=kb)
        return

    total_days, years, months, days = days_together_breakdown(couple.anniversary_date)
    parts = []
    if years:
        parts.append(f"{years}y")
    if months:
        parts.append(f"{months}o")
    parts.append(f"{days}k")
    breakdown_text = " ".join(parts)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=t(lang, "days_change_btn"), callback_data="days:set")], [home_button(lang)]]
    )
    await message.answer(t(lang, "days_together", total=total_days, breakdown=breakdown_text), reply_markup=kb)


@router.callback_query(F.data == "days:set")
async def days_set_start(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.set_state(DaysStates.waiting_date)
    await callback.message.answer(t(db_user.language, "days_ask"))
    await callback.answer()


@router.message(DaysStates.waiting_date, F.text)
async def days_date_received(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    try:
        parsed = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
    except ValueError:
        await message.answer(t(lang, "days_ask"))
        return

    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await state.clear()
        await message.answer("❌")
        return

    await set_anniversary_date(session, couple.id, parsed)
    await state.clear()
    await message.answer(t(lang, "days_saved", date=parsed.strftime("%d.%m.%Y")))

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        try:
            await message.bot.send_message(
                partner.telegram_id, t(partner.language, "days_saved", date=parsed.strftime("%d.%m.%Y"))
            )
        except Exception:
            pass
