"""
🎁 Sovg'a yuborish bo'limi.
"""
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import create_gift_transaction, get_all_gifts, get_couple_for_user, get_gift_by_id, get_partner_user
from utils.helpers import home_button

router = Router(name="gifts")


@router.message(F.text.in_({"🎁 Sovg'a yuborish", "🎁 Virtual sovg'alar"}))
async def gifts_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer("❌ Avval juftingiz bilan ulanishingiz kerak.")
        return

    gifts = await get_all_gifts(session)
    buttons = [[InlineKeyboardButton(text=f"{g.emoji} {g.name}", callback_data=f"gift:select:{g.id}")] for g in gifts]
    buttons.append([home_button()])
    await message.answer("🎁 Sovg'a tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))


@router.callback_query(F.data.startswith("gift:select:"))
async def gift_select(callback: CallbackQuery, session: AsyncSession) -> None:
    gift_id = int(callback.data.split(":")[2])
    gift = await get_gift_by_id(session, gift_id)
    if gift is None:
        await callback.answer("❌ Sovg'a topilmadi.", show_alert=True)
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📤 Yuborish", callback_data=f"gift:send:{gift.id}"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="gift:cancel"),
            ]
        ]
    )
    await callback.message.edit_text(
        f"🎁 Siz:\n{gift.emoji} {gift.name}\nsovg'asini juftingizga yubormoqchisiz.", reply_markup=kb
    )
    await callback.answer()


@router.callback_query(F.data == "gift:cancel")
async def gift_cancel(callback: CallbackQuery) -> None:
    await callback.message.edit_text("❌ Bekor qilindi.")
    await callback.answer()


@router.callback_query(F.data.startswith("gift:send:"))
async def gift_send(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    gift_id = int(callback.data.split(":")[2])
    gift = await get_gift_by_id(session, gift_id)
    couple = await get_couple_for_user(session, db_user.id)
    if gift is None or couple is None:
        await callback.answer("❌ Xatolik yuz berdi.", show_alert=True)
        return

    await create_gift_transaction(session, couple.id, db_user.id, gift.id)

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        try:
            await callback.bot.send_message(
                partner.telegram_id, f"🎁 Sizga juftingizdan sovg'a keldi!\n\n{gift.emoji} {gift.name}"
            )
        except Exception:
            pass

    await callback.message.edit_text("✅ Sovg'a yuborildi!")
    await callback.answer()
