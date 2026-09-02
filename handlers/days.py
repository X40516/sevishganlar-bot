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
from utils.helpers import days_together_breakdown, home_button

router = Router(name="days")


@router.message(F.text == "❤️ Birga bo'lgan kunlar")
async def days_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer("❌ Avval juftingiz bilan ulanishingiz kerak.")
        return

    if couple.anniversary_date is None:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="📅 Sanani belgilash", callback_data="days:set")], [home_button()]]
        )
        await message.answer("❤️ Birga bo'lgan sanangizni belgilang.", reply_markup=kb)
        return

    total_days, years, months, days = days_together_breakdown(couple.anniversary_date)
    parts = []
    if years:
        parts.append(f"{years} yil")
    if months:
        parts.append(f"{months} oy")
    parts.append(f"{days} kun")
    breakdown_text = " ".join(parts)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📅 Sanani o'zgartirish", callback_data="days:set")], [home_button()]]
    )
    await message.answer(
        f"❤️ Sizlar birga bo'lganingizga:\n{total_days} kun\n{breakdown_text}", reply_markup=kb
    )


@router.callback_query(F.data == "days:set")
async def days_set_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(DaysStates.waiting_date)
    await callback.message.answer("📅 Sanani kiriting (KK.OO.YYYY formatida, masalan: 01.05.2023):")
    await callback.answer()


@router.message(DaysStates.waiting_date, F.text)
async def days_date_received(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    try:
        parsed = datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
    except ValueError:
        await message.answer("❌ Sana formati noto'g'ri. Masalan: 01.05.2023 ko'rinishida kiriting.")
        return

    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await state.clear()
        await message.answer("❌ Juftlik topilmadi.")
        return

    await set_anniversary_date(session, couple.id, parsed)
    await state.clear()
    await message.answer(f"✅ Sana saqlandi: {parsed.strftime('%d.%m.%Y')}")

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        try:
            await message.bot.send_message(
                partner.telegram_id, f"❤️ Juftingiz birga bo'lgan sanangizni belgiladi: {parsed.strftime('%d.%m.%Y')}"
            )
        except Exception:
            pass
