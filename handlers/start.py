"""
/start buyrug'i, deep-link orqali juftlikka qo'shilish, asosiy menyu.
"""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import (
    create_couple,
    get_couple_for_user,
    get_invite_by_code,
    get_partner_user,
    get_user_by_id,
    mark_invite_used,
)
from keyboards.reply import MAIN_MENU_KB

router = Router(name="start")


async def show_home(message: Message, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(
            "❤️ Xush kelibsiz, @JuftimBotbot ga!\n\n"
            "Bu bot orqali juftingiz bilan:\n"
            "💌 xatlar yuborishingiz\n"
            "🎲 o'yinlar o'ynashingiz\n"
            "💭 savollarga javob berishingiz\n"
            "🎁 virtual sovg'alar yuborishingiz\n"
            "📸 xotiralar saqlashingiz mumkin.\n\n"
            "Boshlash uchun '💑 Juftimni ulash' tugmasini bosing.",
            reply_markup=MAIN_MENU_KB,
        )
    else:
        await message.answer("🏠 Asosiy menyu:", reply_markup=MAIN_MENU_KB)


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, db_user: User) -> None:
    args = message.text.split(maxsplit=1)
    payload = args[1].strip() if len(args) > 1 else None

    if payload:
        couple = await get_couple_for_user(session, db_user.id)
        if couple is not None:
            await message.answer("❤️ Siz allaqachon juftlikka ulangansiz.", reply_markup=MAIN_MENU_KB)
            return

        invite = await get_invite_by_code(session, payload)
        if invite is None:
            await message.answer("❌ Bu taklif havolasi yaroqsiz yoki muddati o'tgan.")
            await show_home(message, session, db_user)
            return

        if invite.inviter_id == db_user.id:
            await message.answer("❌ O'zingizni o'zingiz taklif qila olmaysiz.")
            await show_home(message, session, db_user)
            return

        inviter = await get_user_by_id(session, invite.inviter_id)
        inviter_couple = await get_couple_for_user(session, invite.inviter_id) if inviter else None
        if inviter is None or inviter_couple is not None:
            await message.answer("❌ Bu taklif endi yaroqsiz.")
            await show_home(message, session, db_user)
            return

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="❤️ Qabul qilish", callback_data=f"invite_accept:{invite.code}"),
                    InlineKeyboardButton(text="❌ Rad etish", callback_data=f"invite_reject:{invite.code}"),
                ]
            ]
        )
        await message.answer(
            f"❤️ Sizni {inviter.full_name} juftlikka qo'shilishga taklif qildi. Qabul qilasizmi?",
            reply_markup=kb,
        )
        return

    await show_home(message, session, db_user)


@router.callback_query(F.data.startswith("invite_accept:"))
async def on_invite_accept(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    code = callback.data.split(":", 1)[1]
    invite = await get_invite_by_code(session, code)
    if invite is None:
        await callback.answer("❌ Bu taklif endi yaroqsiz.", show_alert=True)
        return

    existing_couple = await get_couple_for_user(session, db_user.id)
    inviter_couple = await get_couple_for_user(session, invite.inviter_id)
    if existing_couple is not None or inviter_couple is not None:
        await callback.answer("❌ Bu taklif endi yaroqsiz.", show_alert=True)
        return

    await create_couple(session, invite.inviter_id, db_user.id)
    await mark_invite_used(session, invite)

    await callback.message.edit_text("🎉 Tabriklaymiz!\n❤️ Juftlik muvaffaqiyatli ulandi!")
    await callback.message.answer("🏠 Asosiy menyu:", reply_markup=MAIN_MENU_KB)

    inviter = await get_user_by_id(session, invite.inviter_id)
    if inviter:
        try:
            await callback.bot.send_message(
                inviter.telegram_id,
                "🎉 Tabriklaymiz!\n❤️ Juftlik muvaffaqiyatli ulandi!",
                reply_markup=MAIN_MENU_KB,
            )
        except Exception:
            pass
    await callback.answer()


@router.callback_query(F.data.startswith("invite_reject:"))
async def on_invite_reject(callback: CallbackQuery, session: AsyncSession) -> None:
    await callback.message.edit_text("❌ Taklif rad etildi.")
    await callback.answer()


@router.message(F.text.in_({"ℹ️ Yordam", "❓ Bot qanday ishlaydi?"}))
async def how_it_works(message: Message) -> None:
    await message.answer(
        "ℹ️ @JuftimBotbot qanday ishlaydi:\n\n"
        "1️⃣ '💑 Juftimni ulash' tugmasini bosing va taklif havolasini oling.\n"
        "2️⃣ Havolani sevgilingizga yuboring.\n"
        "3️⃣ U havolani ochib, taklifni qabul qilsin.\n"
        "4️⃣ Endi ikkalangiz xatlar, o'yinlar, sovg'alar va xotiralar orqali muloqot qila olasiz!\n\n"
        "Buyruqlar:\n"
        "/start — botni qayta boshlash\n"
        "/admin — admin panel (faqat administratorlar uchun)"
    )


@router.callback_query(F.data == "menu:home")
async def go_home(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await callback.message.answer("🏠 Asosiy menyu:", reply_markup=MAIN_MENU_KB)
    await callback.answer()
