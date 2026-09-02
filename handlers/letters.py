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
from services.content import LOVE_MESSAGES
from utils.helpers import home_button

router = Router(name="letters")


def _letters_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Matnli xat", callback_data="letter:text")],
            [InlineKeyboardButton(text="📸 Rasm + xabar", callback_data="letter:photo")],
            [InlineKeyboardButton(text="❤️ Sevgi xabari", callback_data="letter:love")],
            [home_button()],
        ]
    )


def _confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📤 Yuborish", callback_data="letter:send"),
                InlineKeyboardButton(text="✏️ O'zgartirish", callback_data="letter:edit"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="letter:cancel")],
        ]
    )


async def _require_couple(message: Message, session: AsyncSession, db_user: User):
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer("❌ Avval juftingiz bilan ulanishingiz kerak.")
        return None
    return couple


@router.message(F.text == "💌 Xat yuborish")
@router.callback_query(F.data == "goto:letters")
async def letters_menu(event, session: AsyncSession, db_user: User) -> None:
    message = event.message if isinstance(event, CallbackQuery) else event
    couple = await _require_couple(message, session, db_user)
    if couple is None:
        if isinstance(event, CallbackQuery):
            await event.answer()
        return
    await message.answer("💌 Juftingizga nima yubormoqchisiz?", reply_markup=_letters_menu_kb())
    if isinstance(event, CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "letter:text")
async def letter_text_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LetterStates.waiting_text)
    await state.update_data(letter_type="text")
    await callback.message.answer("✍️ Matningizni yozing:")
    await callback.answer()


@router.callback_query(F.data == "letter:photo")
async def letter_photo_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LetterStates.waiting_photo)
    await state.update_data(letter_type="photo")
    await callback.message.answer("📸 Rasm yuboring (izoh bilan birga yuborishingiz mumkin):")
    await callback.answer()


@router.callback_query(F.data == "letter:love")
async def letter_love(callback: CallbackQuery, state: FSMContext) -> None:
    text = random.choice(LOVE_MESSAGES)
    await state.set_state(LetterStates.confirm)
    await state.update_data(letter_type="love_message", content=text, photo_file_id=None)
    await callback.message.answer(f"💌 Xatingiz:\n\n{text}\n\nJuftingizga yuborilsinmi?", reply_markup=_confirm_kb())
    await callback.answer()


@router.message(LetterStates.waiting_text, F.text)
async def letter_text_received(message: Message, state: FSMContext) -> None:
    await state.update_data(content=message.text, photo_file_id=None)
    await state.set_state(LetterStates.confirm)
    await message.answer(f"💌 Xatingiz:\n\n{message.text}\n\nJuftingizga yuborilsinmi?", reply_markup=_confirm_kb())


@router.message(LetterStates.waiting_photo, F.photo)
async def letter_photo_received(message: Message, state: FSMContext) -> None:
    photo_file_id = message.photo[-1].file_id
    caption = message.caption or ""
    await state.update_data(content=caption, photo_file_id=photo_file_id)
    await state.set_state(LetterStates.confirm)
    preview = f"📸 Rasm + izoh:\n{caption}" if caption else "📸 Rasm (izohsiz)"
    await message.answer(f"{preview}\n\nJuftingizga yuborilsinmi?", reply_markup=_confirm_kb())


@router.callback_query(F.data == "letter:edit")
async def letter_edit(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    letter_type = data.get("letter_type", "text")
    if letter_type == "text":
        await state.set_state(LetterStates.waiting_text)
        await callback.message.answer("✍️ Matningizni qaytadan yozing:")
    elif letter_type == "photo":
        await state.set_state(LetterStates.waiting_photo)
        await callback.message.answer("📸 Rasmni qaytadan yuboring:")
    else:
        text = random.choice(LOVE_MESSAGES)
        await state.update_data(content=text)
        await callback.message.answer(f"💌 Xatingiz:\n\n{text}\n\nJuftingizga yuborilsinmi?", reply_markup=_confirm_kb())
    await callback.answer()


@router.callback_query(F.data == "letter:cancel")
async def letter_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Bekor qilindi.")
    await callback.answer()


@router.callback_query(F.data == "letter:send")
async def letter_send(callback: CallbackQuery, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌ Juftlik topilmadi.", show_alert=True)
        await state.clear()
        return

    data = await state.get_data()
    letter_type = data.get("letter_type", "text")
    content = data.get("content", "")
    photo_file_id = data.get("photo_file_id")

    await create_letter(session, couple.id, db_user.id, letter_type, content, photo_file_id)

    partner = await get_partner_user(session, couple, db_user.id)
    reply_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❤️ Javob berish", callback_data="goto:letters")]]
    )
    if partner:
        try:
            if letter_type == "photo" and photo_file_id:
                caption = f"💌 Sizga juftingizdan yangi xat keldi!\n\n{content}" if content else "💌 Sizga juftingizdan yangi xat keldi!"
                await callback.bot.send_photo(partner.telegram_id, photo_file_id, caption=caption, reply_markup=reply_kb)
            else:
                await callback.bot.send_message(
                    partner.telegram_id, f"💌 Sizga juftingizdan yangi xat keldi!\n\n{content}", reply_markup=reply_kb
                )
        except Exception:
            pass

    await state.clear()
    await callback.message.edit_text("✅ Xat yuborildi!")
    await callback.answer()
