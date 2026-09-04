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
from keyboards.reply import MENU_TEXTS
from locales.texts import t
from utils.helpers import home_button

router = Router(name="questions")


def _question_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "question_answer_btn"), callback_data="q:answer")],
            [InlineKeyboardButton(text=t(lang, "question_view_btn"), callback_data="q:view_partner")],
            [InlineKeyboardButton(text=t(lang, "question_another_btn"), callback_data="q:another")],
            [home_button(lang)],
        ]
    )


@router.message(F.text.in_(MENU_TEXTS["menu_question"]))
async def question_menu(message: Message, session: AsyncSession, db_user: User, state: FSMContext) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "no_couple"))
        return

    question = await get_todays_question(session, couple.id, date.today())
    await state.update_data(display_question=question.text)
    await message.answer(t(lang, "question_prompt", question=question.text), reply_markup=_question_kb(lang))


@router.callback_query(F.data == "q:another")
async def question_another(callback: CallbackQuery, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    questions = await get_all_daily_questions(session)
    new_question = random.choice(questions).text
    await state.update_data(display_question=new_question)
    await callback.message.edit_text(t(lang, "question_prompt", question=new_question), reply_markup=_question_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "q:answer")
async def question_answer_start(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.set_state(QuestionStates.answering)
    await callback.message.answer(t(db_user.language, "question_write_answer"))
    await callback.answer()


@router.message(QuestionStates.answering, F.text)
async def question_answer_received(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await state.clear()
        await message.answer("❌")
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
            f"✅\n\n💭 {question.text}\n\n👤 {message.text}\n❤️ {partner_answer.answer_text}"
        )
        if partner:
            try:
                await message.bot.send_message(
                    partner.telegram_id,
                    f"🎉\n\n💭 {question.text}\n\n❤️ {partner_answer.answer_text}\n👤 {message.text}",
                )
            except Exception:
                pass
    else:
        await message.answer(t(lang, "question_saved_waiting"))


@router.callback_query(F.data == "q:view_partner")
async def question_view_partner(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌", show_alert=True)
        return

    today = date.today()
    self_answer = await get_answer_for_today(session, couple.id, db_user.id, today)
    if self_answer is None:
        await callback.answer("...", show_alert=True)
        return

    partner = await get_partner_user(session, couple, db_user.id)
    partner_answer = await get_answer_for_today(session, couple.id, partner.id, today) if partner else None
    if partner_answer is None:
        await callback.answer("...", show_alert=True)
        return

    await callback.message.answer(
        f"💭 {self_answer.question_text}\n\n👤 {self_answer.answer_text}\n❤️ {partner_answer.answer_text}"
    )
    await callback.answer()
