"""
🎵 Qo'shiq yuborish bo'limi - YouTube havolasini qidirib, juftga yuborish.
Video/audio yuklab olinmaydi, faqat havola yuboriladi.
"""
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import get_couple_for_user, get_partner_user
from handlers.states import MusicStates
from keyboards.reply import MENU_TEXTS
from locales.texts import t
from services.youtube import search_youtube
from utils.helpers import home_button

router = Router(name="music")


@router.message(F.text.in_(MENU_TEXTS["menu_music"]))
async def music_start(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "no_couple"))
        return
    await state.set_state(MusicStates.waiting_query)
    await message.answer(t(lang, "music_ask_query"))


@router.message(MusicStates.waiting_query, F.text)
async def music_query_received(message: Message, state: FSMContext, db_user: User) -> None:
    lang = db_user.language
    title, url = await search_youtube(message.text.strip())
    await state.update_data(title=title, url=url)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "letters_send_btn"), callback_data="music:send"),
                InlineKeyboardButton(text=t(lang, "letters_cancel_btn"), callback_data="music:cancel"),
            ],
            [home_button(lang)],
        ]
    )
    await message.answer(t(lang, "music_preview", title=title, url=url), reply_markup=kb)


@router.callback_query(F.data == "music:cancel")
async def music_cancel(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.clear()
    await callback.message.edit_text(t(db_user.language, "letters_cancelled"))
    await callback.answer()


@router.callback_query(F.data == "music:send")
async def music_send(callback: CallbackQuery, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌", show_alert=True)
        await state.clear()
        return

    data = await state.get_data()
    title = data.get("title", "")
    url = data.get("url", "")

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        try:
            header = t(partner.language, "music_received")
            await callback.bot.send_message(partner.telegram_id, f"{header}\n\n{title}\n{url}")
        except Exception:
            pass

    await state.clear()
    await callback.message.edit_text(t(lang, "music_sent"))
    await callback.answer()
