"""
Foydalanuvchini DBga yozib/topib beruvchi va ban holatini tekshiruvchi middleware.
"""
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from config import ADMIN_ID
from database.queries import get_or_create_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        if tg_user is None:
            return await handler(event, data)

        session = data["session"]
        db_user = await get_or_create_user(
            session,
            telegram_id=tg_user.id,
            full_name=tg_user.full_name or "",
            username=tg_user.username,
        )
        data["db_user"] = db_user

        if db_user.is_banned and tg_user.id != ADMIN_ID:
            if isinstance(event, Message):
                await event.answer("🚫 Siz botdan foydalana olmaysiz.")
            elif isinstance(event, CallbackQuery):
                await event.answer("🚫 Siz botdan foydalana olmaysiz.", show_alert=True)
            return None

        return await handler(event, data)
