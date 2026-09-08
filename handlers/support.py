"""
🫂 Dardlashamiz bo'limi - juftlik holatidan qat'iy nazar ishlaydi.
Hissiy qo'llab-quvvatlash, hukm qilmasdan tinglash.
"""
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from keyboards.reply import MENU_TEXTS
from handlers.states import SupportStates
from locales.texts import t
from services.support_content import get_support_response

router = Router(name="support")


@router.message(F.text.in_(MENU_TEXTS["menu_support"]))
async def support_start(message: Message, state: FSMContext, db_user: User) -> None:
    await state.set_state(SupportStates.chatting)
    await state.update_data(last_category=None)
    await message.answer(t(db_user.language, "support_intro"))


@router.message(SupportStates.chatting, F.text)
async def support_chat(message: Message, state: FSMContext, db_user: User) -> None:
    reply_text, new_category = get_support_response(message.text, (await state.get_data()).get("last_category"))
    await state.update_data(last_category=new_category)
    await message.answer(reply_text)
