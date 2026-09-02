"""
💭 Bugungi savol bo'limi.
"""
import random
from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import (
    get_all_daily_questions,
    get_answer_for_today,
    get_couple_for_user,
    get_partner_user,
    get_todays_question,
    save_question_answer,
)
from handlers.states import QuestionStates
from utils.helpers import home_button

router = Router(name="questions")


def _question_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Javob berish", callback_data="q:answer")],
            [InlineKeyboardButton(text="👀 Juftimning javobini ko'rish", callback_data="q:view_partner")],
            [InlineKeyboardButton(text="🔄 Boshqa savol", callback_data="q:another")],
            [home_button()],
        ]
    )


@router.message(F.text == "💭 Bugungi savol")
async def question_menu(message: Message, session: AsyncSession, db_user: User, state: FSMContext) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer("❌ Avval juftingiz bilan ulanishingiz kerak.")
        return

    question = await get_todays_question(session, couple.id, date.today())
    await state.update_data(display_question=question.text)
    await message.answer(f"💭 Bugungi savol:\n{question.text}", reply_markup=_question_kb())


@router.callback_query(F.data == "q:another")
async def question_another(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    questions = await get_all_daily_questions(session)
    new_question = random.choice(questions).text
    await state.update_data(display_question=new_question)
    await callback.message.edit_text(
        f"💭 Muqobil savol (ilhom uchun):\n{new_question}\n\n"
        "ℹ️ Javobingiz baribir kunning asosiy savoliga tegishli bo'ladi, shunda juftingiz bilan solishtira olasiz.",
        reply_markup=_question_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "q:answer")
async def question_answer_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(QuestionStates.answering)
    await callback.message.answer("✍️ Javobingizni yozing:")
    await callback.answer()


@router.message(QuestionStates.answering, F.text)
async def question_answer_received(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await state.clear()
        await message.answer("❌ Juftlik topilmadi.")
        return

    today = date.today()
    question = await get_todays_question(session, couple.id, today)
    await save_question_answer(session, couple.id, db_user.id, question, today, message.text)
    await state.clear()

    partner = await get_partner_user(session, couple, db_user.id)
    partner_answer = None
    if partner:
        partner_answer = await get_answer_for_today(session, couple.id, partner.id, today)

    if partner_answer:
        await message.answer(
            f"✅ Javobingiz saqlandi!\n\n"
            f"💭 Savol: {question.text}\n\n"
            f"👤 Sizning javobingiz: {message.text}\n"
            f"❤️ Juftingizning javobi: {partner_answer.answer_text}"
        )
        if partner:
            try:
                await message.bot.send_message(
                    partner.telegram_id,
                    f"🎉 Juftingiz ham bugungi savolga javob berdi!\n\n"
                    f"💭 Savol: {question.text}\n\n"
                    f"❤️ Sizning javobingiz: {partner_answer.answer_text}\n"
                    f"👤 Juftingizning javobi: {message.text}",
                )
            except Exception:
                pass
    else:
        await message.answer("✅ Javobingiz saqlandi! Juftingiz javob berishini kutmoqdamiz. 💭")


@router.callback_query(F.data == "q:view_partner")
async def question_view_partner(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌ Juftlik topilmadi.", show_alert=True)
        return

    today = date.today()
    self_answer = await get_answer_for_today(session, couple.id, db_user.id, today)
    if self_answer is None:
        await callback.answer("Avval siz javob bering.", show_alert=True)
        return

    partner = await get_partner_user(session, couple, db_user.id)
    partner_answer = await get_answer_for_today(session, couple.id, partner.id, today) if partner else None
    if partner_answer is None:
        await callback.answer("Juftingiz hali javob bermagan.", show_alert=True)
        return

    await callback.message.answer(
        f"💭 Savol: {self_answer.question_text}\n\n"
        f"👤 Sizning javobingiz: {self_answer.answer_text}\n"
        f"❤️ Juftingizning javobi: {partner_answer.answer_text}"
    )
    await callback.answer()
