"""
💌 Xat yuborish bo'limi: matnli xat, rasm+xabar, tayyor sevgi xabari.
"""
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import create_letter, get_couple_for_user, get_partner_user
from handlers.states import LetterStates
from keyboards.reply import MENU_TEXTS
from locales.texts import t
from services.content import LOVE_MESSAGES
from utils.helpers import home_button

router = Router(name="letters")


def _letters_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "letters_text_btn"), callback_data="letter:text")],
            [InlineKeyboardButton(text=t(lang, "letters_photo_btn"), callback_data="letter:photo")],
            [InlineKeyboardButton(text=t(lang, "letters_love_btn"), callback_data="letter:love")],
            [home_button(lang)],
        ]
    )


def _confirm_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "letters_send_btn"), callback_data="letter:send"),
                InlineKeyboardButton(text=t(lang, "letters_edit_btn"), callback_data="letter:edit"),
            ],
            [InlineKeyboardButton(text=t(lang, "letters_cancel_btn"), callback_data="letter:cancel")],
        ]
    )


async def _require_couple(message: Message, session: AsyncSession, db_user: User):
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(db_user.language, "no_couple"))
        return None
    return couple


@router.message(F.text.in_(MENU_TEXTS["menu_letter"]))
@router.callback_query(F.data == "goto:letters")
async def letters_menu(event, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    message = event.message if isinstance(event, CallbackQuery) else event
    couple = await _require_couple(message, session, db_user)
    if couple is None:
        if isinstance(event, CallbackQuery):
            await event.answer()
        return
    await message.answer(t(lang, "letters_prompt"), reply_markup=_letters_menu_kb(lang))
    if isinstance(event, CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "letter:text")
async def letter_text_start(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.set_state(LetterStates.waiting_text)
    await state.update_data(letter_type="text")
    await callback.message.answer(t(db_user.language, "letters_write_text"))
    await callback.answer()


@router.callback_query(F.data == "letter:photo")
async def letter_photo_start(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.set_state(LetterStates.waiting_photo)
    await state.update_data(letter_type="photo")
    await callback.message.answer(t(db_user.language, "letters_send_photo"))
    await callback.answer()


@router.callback_query(F.data == "letter:love")
async def letter_love(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    lang = db_user.language
    text = random.choice(LOVE_MESSAGES)
    await state.set_state(LetterStates.confirm)
    await state.update_data(letter_type="love_message", content=text, photo_file_id=None)
    await callback.message.answer(t(lang, "letters_preview", text=text), reply_markup=_confirm_kb(lang))
    await callback.answer()


@router.message(LetterStates.waiting_text, F.text)
async def letter_text_received(message: Message, state: FSMContext, db_user: User) -> None:
    lang = db_user.language
    await state.update_data(content=message.text, photo_file_id=None)
    await state.set_state(LetterStates.confirm)
    await message.answer(t(lang, "letters_preview", text=message.text), reply_markup=_confirm_kb(lang))


@router.message(LetterStates.waiting_photo, F.photo)
async def letter_photo_received(message: Message, state: FSMContext, db_user: User) -> None:
    lang = db_user.language
    photo_file_id = message.photo[-1].file_id
    caption = message.caption or ""
    await state.update_data(content=caption, photo_file_id=photo_file_id)
    await state.set_state(LetterStates.confirm)
    preview_text = caption if caption else "📸"
    await message.answer(t(lang, "letters_preview", text=preview_text), reply_markup=_confirm_kb(lang))


@router.callback_query(F.data == "letter:edit")
async def letter_edit(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    lang = db_user.language
    data = await state.get_data()
    letter_type = data.get("letter_type", "text")
    if letter_type == "text":
        await state.set_state(LetterStates.waiting_text)
        await callback.message.answer(t(lang, "letters_write_text"))
    elif letter_type == "photo":
        await state.set_state(LetterStates.waiting_photo)
        await callback.message.answer(t(lang, "letters_send_photo"))
    else:
        text = random.choice(LOVE_MESSAGES)
        await state.update_data(content=text)
        await callback.message.answer(t(lang, "letters_preview", text=text), reply_markup=_confirm_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "letter:cancel")
async def letter_cancel(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.clear()
    await callback.message.edit_text(t(db_user.language, "letters_cancelled"))
    await callback.answer()


@router.callback_query(F.data == "letter:send")
async def letter_send(callback: CallbackQuery, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌", show_alert=True)
        await state.clear()
        return

    data = await state.get_data()
    letter_type = data.get("letter_type", "text")
    content = data.get("content", "")
    photo_file_id = data.get("photo_file_id")

    await create_letter(session, couple.id, db_user.id, letter_type, content, photo_file_id)

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        reply_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=t(partner.language, "letters_reply_btn"), callback_data="goto:letters")]]
        )
        try:
            header = t(partner.language, "letters_received")
            if letter_type == "photo" and photo_file_id:
                caption = f"{header}\n\n{content}" if content else header
                await callback.bot.send_photo(partner.telegram_id, photo_file_id, caption=caption, reply_markup=reply_kb)
            else:
                await callback.bot.send_message(partner.telegram_id, f"{header}\n\n{content}", reply_markup=reply_kb)
        except Exception:
            pass

    await state.clear()
    await callback.message.edit_text(t(lang, "letters_sent"))
    await callback.answer()
