"""
📸 Xotiralar bo'limi.
"""
from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import add_memory, delete_memory, get_couple_for_user, get_memories, get_partner_user
from handlers.states import MemoryStates
from keyboards.reply import MENU_TEXTS
from locales.texts import t
from utils.helpers import home_button

router = Router(name="memories")


def _memories_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t(lang, "memories_add_btn"), callback_data="mem:add")],
            [InlineKeyboardButton(text=t(lang, "memories_view_btn"), callback_data="mem:view:0")],
            [InlineKeyboardButton(text=t(lang, "memories_delete_btn"), callback_data="mem:delete_menu")],
            [home_button(lang)],
        ]
    )


@router.message(F.text.in_(MENU_TEXTS["menu_memories"]))
@router.callback_query(F.data == "goto:memories")
async def memories_menu(event, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    message = event.message if isinstance(event, CallbackQuery) else event
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "no_couple"))
        if isinstance(event, CallbackQuery):
            await event.answer()
        return
    await message.answer(t(lang, "memories_prompt"), reply_markup=_memories_menu_kb(lang))
    if isinstance(event, CallbackQuery):
        await event.answer()


@router.callback_query(F.data == "mem:add")
async def mem_add_start(callback: CallbackQuery, state: FSMContext, db_user: User) -> None:
    await state.set_state(MemoryStates.waiting_photo)
    await callback.message.answer(t(db_user.language, "memory_send_photo"))
    await callback.answer()


@router.message(MemoryStates.waiting_photo, F.photo)
async def mem_photo_received(message: Message, state: FSMContext, db_user: User) -> None:
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)
    await state.set_state(MemoryStates.waiting_caption)
    await message.answer(t(db_user.language, "memory_send_caption"))


@router.message(MemoryStates.waiting_caption, F.text)
async def mem_caption_received(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await state.clear()
        await message.answer("❌")
        return

    data = await state.get_data()
    caption = "" if message.text.strip() == "-" else message.text.strip()
    await add_memory(session, couple.id, db_user.id, data["photo_file_id"], caption, date.today())
    await state.clear()
    await message.answer(t(lang, "memory_saved"))

    partner = await get_partner_user(session, couple, db_user.id)
    if partner:
        try:
            cap = f"📸\n{caption}" if caption else "📸"
            await message.bot.send_photo(partner.telegram_id, data["photo_file_id"], caption=cap)
        except Exception:
            pass


@router.callback_query(F.data.startswith("mem:view:"))
async def mem_view(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    offset = int(callback.data.split(":")[2])
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌", show_alert=True)
        return

    memories = await get_memories(session, couple.id)
    if not memories:
        await callback.message.answer("📭")
        await callback.answer()
        return

    offset = max(0, min(offset, len(memories) - 1))
    memory = memories[offset]

    nav_buttons = []
    if offset > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"mem:view:{offset - 1}"))
    if offset < len(memories) - 1:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"mem:view:{offset + 1}"))

    kb = InlineKeyboardMarkup(inline_keyboard=[nav_buttons] if nav_buttons else [])
    caption = f"📅 {memory.memory_date.strftime('%d.%m.%Y')}\n{memory.caption}" if memory.caption else f"📅 {memory.memory_date.strftime('%d.%m.%Y')}"
    caption += f"\n\n({offset + 1}/{len(memories)})"

    await callback.message.answer_photo(memory.photo_file_id, caption=caption, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "mem:delete_menu")
async def mem_delete_menu(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌", show_alert=True)
        return

    memories = await get_memories(session, couple.id)
    if not memories:
        await callback.message.answer("📭")
        await callback.answer()
        return

    buttons = [
        [InlineKeyboardButton(text=f"🗑 {m.memory_date.strftime('%d.%m.%Y')} - {m.caption[:20] or '-'}", callback_data=f"mem:delete:{m.id}")]
        for m in memories[:20]
    ]
    await callback.message.answer("🗑", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await callback.answer()


@router.callback_query(F.data.startswith("mem:delete:"))
async def mem_delete(callback: CallbackQuery, session: AsyncSession) -> None:
    memory_id = int(callback.data.split(":")[2])
    await delete_memory(session, memory_id)
    await callback.message.edit_text("✅")
    await callback.answer()
