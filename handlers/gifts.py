"""
🎁 Sovg'a yuborish bo'limi.
"""
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import create_gift_transaction, get_all_gifts, get_couple_for_user, get_gift_by_id, get_partner_user
from keyboards.reply import MENU_TEXTS
from locales.texts import t
from utils.helpers import home_button

router = Router(name="gifts")


@router.message(F.text.in_(MENU_TEXTS["menu_gift"]))
async def gifts_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "no_couple"))
        return

    gifts = await get_all_gifts(session)
    buttons = [[InlineKeyboardButton(text=f"{g.emoji} {g.name}", callback_data=f"gift:select:{g.id}")] for g in gifts]
    buttons.append([home_button(lang)])
    await message.answer(t(lang, "gifts_prompt"), reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data.startswith("gift:select:"))
async def gift_select(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    gift_id = int(callback.data.split(":")[2])
    gift = await get_gift_by_id(session, gift_id)
    if gift is None:
        await callback.answer("❌", show_alert=True)
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t(lang, "letters_send_btn"), callback_data=f"gift:send:{gift.id}"),
                InlineKeyboardButton(text=t(lang, "letters_cancel_btn"), callback_data="gift:cancel"),
            ]
        ]
    )
    await callback.message.edit_text(f"🎁 {gift.emoji} {gift.name}", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "gift:cancel")
async def gift_cancel(callback: CallbackQuery, db_user: User) -> None:
    await callback.message.edit_text(t(db_user.language, "letters_cancelled"))
    await callback.answer()


@router.callback_query(F.data.startswith("gift:send:"))
async def gift_send(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    gift_id = int(callback.data.split(":")[2])
    gift = await get_gift_by_id(session, gift_id)
    couple = await get_couple_for_user(session, db_user.id)
    if gift is None or couple is None:
        await callback.answer("❌", show_alert=True)
        return

    await create_gift_transaction(session, couple.id, db_user.id, gift.id)

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        try:
            await callback.bot.send_message(
                partner.telegram_id, t(partner.language, "gift_received", emoji=gift.emoji, name=gift.name)
            )
        except Exception:
            pass

    await callback.message.edit_text(t(lang, "gift_sent"))
    await callback.answer()
