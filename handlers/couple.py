"""
❤️ Juftim bo'limi: ulanish, kod, ma'lumot, ajratish.
"""
from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import create_pair_invite, deactivate_couple, get_couple_for_user, get_partner_user
from keyboards.reply import MAIN_MENU_KB
from utils.helpers import days_together_breakdown, home_button

router = Router(name="couple")


def _no_couple_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Taklif havolasi", callback_data="couple:link")],
            [InlineKeyboardButton(text="📋 Kodim", callback_data="couple:code")],
            [home_button()],
        ]
    )


def _couple_info_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📅 Sanani belgilash", callback_data="days:set")],
            [InlineKeyboardButton(text="💌 Xat yuborish", callback_data="goto:letters")],
            [InlineKeyboardButton(text="📸 Xotiralar", callback_data="goto:memories")],
            [InlineKeyboardButton(text="💔 Juftlikni ajratish", callback_data="couple:unpair_confirm")],
            [home_button()],
        ]
    )


async def show_couple_section(message: Message, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(
            "💑 Juftingizni @JuftimBotbot ga taklif qiling.",
            reply_markup=_no_couple_kb(),
        )
        return

    partner = await get_partner_user(session, couple, db_user.id)
    if couple.anniversary_date:
        total_days, years, months, days = days_together_breakdown(couple.anniversary_date)
        sana_text = f"📅 Birga bo'lgan sana: {couple.anniversary_date.strftime('%d.%m.%Y')}\n❤️ Birga bo'lgan kunlar: {total_days} kun"
    else:
        sana_text = "📅 Birga bo'lgan sana: belgilanmagan"

    await message.answer(
        f"❤️ Sizning juftingiz:\n👤 {partner.full_name}\n{sana_text}",
        reply_markup=_couple_info_kb(),
    )


@router.message(F.text.in_({"❤️ Juftim", "💑 Juftimni ulash"}))
async def couple_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    await show_couple_section(message, session, db_user)


@router.callback_query(F.data == "couple:link")
async def couple_link(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    bot_info = await callback.bot.get_me()
    invite = await create_pair_invite(session, db_user.id)
    link = f"https://t.me/{bot_info.username}?start={invite.code}"
    await callback.message.answer(f"🔗 Taklif havolangiz:\n{link}\n\nBu havolani sevgilingizga yuboring.")
    await callback.answer()


@router.callback_query(F.data == "couple:code")
async def couple_code(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    invite = await create_pair_invite(session, db_user.id)
    await callback.message.answer(
        f"📋 Kodingiz: {invite.code}\n\nJuftingiz botga shu buyruqni yuborsin:\n/start {invite.code}"
    )
    await callback.answer()


@router.callback_query(F.data == "couple:unpair_confirm")
async def couple_unpair_confirm(callback: CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💔 Ha, ajratish", callback_data="couple:unpair_yes"),
                InlineKeyboardButton(text="❌ Yo'q", callback_data="couple:unpair_no"),
            ]
        ]
    )
    await callback.message.edit_text("⚠️ Haqiqatan ham juftlikni ajratmoqchimisiz?", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "couple:unpair_no")
async def couple_unpair_no(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await callback.message.delete()
    await show_couple_section(callback.message, session, db_user)
    await callback.answer()


@router.callback_query(F.data == "couple:unpair_yes")
async def couple_unpair_yes(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌ Juftlik topilmadi.", show_alert=True)
        return
    partner = await get_partner_user(session, couple, db_user.id)
    await deactivate_couple(session, couple.id)

    await callback.message.edit_text("💔 Juftlik ajratildi.")
    await callback.message.answer("💑 Juftingizni @JuftimBotbot ga taklif qiling.", reply_markup=MAIN_MENU_KB)

    if partner:
        try:
            await callback.bot.send_message(
                partner.telegram_id,
                "💔 Juftingiz aloqani uzdi. Yangi juftlik uchun taklif havolasi yaratishingiz mumkin.",
                reply_markup=MAIN_MENU_KB,
            )
        except Exception:
            pass
    await callback.answer()
