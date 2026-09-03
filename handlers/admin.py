"""
👑 Admin panel - faqat ADMIN_ID uchun.
"""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import ADMIN_ID
from database.queries import (
    add_daily_question,
    get_all_gifts,
    get_all_user_telegram_ids,
    get_gift_stats,
    get_latest_couples,
    get_latest_users,
    get_stats,
    get_user_by_telegram_id,
    log_admin_action,
    set_user_ban,
)
from handlers.states import AdminStates
from database.models import Gift

router = Router(name="admin")
router.message.filter(F.from_user.id == ADMIN_ID)
router.callback_query.filter(F.from_user.id == ADMIN_ID)


def _admin_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats")],
            [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin:users")],
            [InlineKeyboardButton(text="💑 Juftliklar", callback_data="admin:couples")],
            [InlineKeyboardButton(text="📢 Broadcast", callback_data="admin:broadcast")],
            [InlineKeyboardButton(text="💭 Savollar", callback_data="admin:questions")],
            [InlineKeyboardButton(text="🎁 Sovg'alar", callback_data="admin:gifts")],
            [InlineKeyboardButton(text="🚫 Ban", callback_data="admin:ban")],
            [InlineKeyboardButton(text="📈 Analitika", callback_data="admin:analytics")],
        ]
    )


@router.message(Command("admin"))
async def admin_menu(message: Message) -> None:
    await message.answer("👑 Admin panel:", reply_markup=_admin_menu_kb())


@router.callback_query(F.data == "admin:stats")
async def admin_stats(callback: CallbackQuery, session: AsyncSession) -> None:
    stats = await get_stats(session)
    await callback.message.edit_text(
        "📊 Statistika:\n\n"
        f"👥 Jami users: {stats['total_users']}\n"
        f"💑 Jami juftliklar: {stats['total_couples']}\n"
        f"❤️ Bugungi faol users: {stats['active_today']}\n"
        f"📈 Haftalik yangi users: {stats['weekly_new']}\n"
        f"📈 Oylik yangi users: {stats['monthly_new']}",
        reply_markup=_admin_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin:users")
async def admin_users(callback: CallbackQuery, session: AsyncSession) -> None:
    users = await get_latest_users(session, limit=10)
    lines = [f"• {u.full_name} (@{u.username or '-'}) — {u.created_at.strftime('%d.%m.%Y')}" for u in users]
    text = "👥 So'nggi 10 foydalanuvchi:\n\n" + "\n".join(lines) if lines else "👥 Foydalanuvchilar yo'q."
    await callback.message.edit_text(text, reply_markup=_admin_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "admin:couples")
async def admin_couples(callback: CallbackQuery, session: AsyncSession) -> None:
    from database.queries import get_user_by_id

    couples = await get_latest_couples(session, limit=10)
    lines = []
    for c in couples:
        u1 = await get_user_by_id(session, c.user1_id)
        u2 = await get_user_by_id(session, c.user2_id)
        lines.append(f"• {u1.full_name} ❤️ {u2.full_name} — {c.created_at.strftime('%d.%m.%Y')}")
    text = "💑 So'nggi 10 juftlik:\n\n" + "\n".join(lines) if lines else "💑 Juftliklar yo'q."
    await callback.message.edit_text(text, reply_markup=_admin_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "admin:broadcast")
async def admin_broadcast_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_broadcast)
    await callback.message.answer("📢 Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yozing:")
    await callback.answer()


@router.message(AdminStates.waiting_broadcast, F.text)
async def admin_broadcast_send(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    telegram_ids = await get_all_user_telegram_ids(session)
    success, failed = 0, 0
    for tg_id in telegram_ids:
        try:
            await message.bot.send_message(tg_id, message.text)
            success += 1
        except Exception:
            failed += 1
    await log_admin_action(session, message.from_user.id, "broadcast", f"success={success} failed={failed}")
    await message.answer(f"✅ Yuborildi: {success}\n❌ Xatolik: {failed}")


@router.callback_query(F.data == "admin:questions")
async def admin_questions(callback: CallbackQuery, session: AsyncSession) -> None:
    from database.queries import get_all_daily_questions

    questions = await get_all_daily_questions(session)
    lines = [f"{i + 1}. {q.text}" for i, q in enumerate(questions[:15])]
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Yangi savol qo'shish", callback_data="admin:add_question")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:back")],
        ]
    )
    await callback.message.edit_text(f"💭 Savollar ({len(questions)} ta):\n\n" + "\n".join(lines), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "admin:add_question")
async def admin_add_question_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_new_question)
    await callback.message.answer("💭 Yangi savol matnini yozing:")
    await callback.answer()


@router.message(AdminStates.waiting_new_question, F.text)
async def admin_add_question_save(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await add_daily_question(session, message.text.strip())
    await state.clear()
    await log_admin_action(session, message.from_user.id, "add_question", message.text.strip())
    await message.answer("✅ Yangi savol qo'shildi!")


@router.callback_query(F.data == "admin:gifts")
async def admin_gifts(callback: CallbackQuery, session: AsyncSession) -> None:
    stats = await get_gift_stats(session)
    lines = [f"{emoji} {name}: {count} marta yuborilgan" for name, emoji, count in stats]
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Yangi sovg'a qo'shish", callback_data="admin:add_gift")],
            [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin:back")],
        ]
    )
    await callback.message.edit_text("🎁 Sovg'alar statistikasi:\n\n" + "\n".join(lines), reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "admin:add_gift")
async def admin_add_gift_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_new_gift)
    await callback.message.answer("🎁 Yangi sovg'ani 'Emoji Nomi' formatida yozing. Masalan: 🎈 Shar")
    await callback.answer()


@router.message(AdminStates.waiting_new_gift, F.text)
async def admin_add_gift_save(message: Message, state: FSMContext, session: AsyncSession) -> None:
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("❌ Format noto'g'ri. Masalan: 🎈 Shar")
        return
    emoji, name = parts
    session.add(Gift(name=name, emoji=emoji))
    await session.commit()
    await state.clear()
    await log_admin_action(session, message.from_user.id, "add_gift", f"{emoji} {name}")
    await message.answer("✅ Yangi sovg'a qo'shildi!")


@router.callback_query(F.data == "admin:ban")
async def admin_ban_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.waiting_ban_target)
    await callback.message.answer("🚫 Ban/unban qilmoqchi bo'lgan foydalanuvchining Telegram ID raqamini yuboring:")
    await callback.answer()


@router.message(AdminStates.waiting_ban_target, F.text)
async def admin_ban_apply(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    try:
        target_tg_id = int(message.text.strip())
    except ValueError:
        await message.answer("❌ Telegram ID raqam bo'lishi kerak.")
        return

    user = await get_user_by_telegram_id(session, target_tg_id)
    if user is None:
        await message.answer("❌ Bunday foydalanuvchi topilmadi.")
        return

    new_status = not user.is_banned
    await set_user_ban(session, user.id, new_status)
    await log_admin_action(session, message.from_user.id, "ban_toggle", f"user={target_tg_id} banned={new_status}")
    status_text = "banlandi 🚫" if new_status else "ban olindi ✅"
    await message.answer(f"{user.full_name} {status_text}")


@router.callback_query(F.data == "admin:analytics")
async def admin_analytics(callback: CallbackQuery, session: AsyncSession) -> None:
    stats = await get_stats(session)
    await callback.message.edit_text(
        "📈 Analitika:\n\n"
        f"💌 Jami xatlar: {stats['total_letters']}\n"
        f"🎁 Jami sovg'alar: {stats['total_gifts']}\n"
        f"📸 Jami xotiralar: {stats['total_memories']}",
        reply_markup=_admin_menu_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == "admin:back")
async def admin_back(callback: CallbackQuery) -> None:
    await callback.message.edit_text("👑 Admin panel:", reply_markup=_admin_menu_kb())
    await callback.answer()
