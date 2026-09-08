"""
Barcha matnli xabarlarni 18+ kontentga tekshiruvchi global middleware.
Aniqlansa, ogohlantirish yuboriladi va xabar keyingi handlerlarga o'tkazilmaydi.
"""
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from locales.texts import t
from utils.content_filter import is_adult_content


class AdultContentMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.text:
            if is_adult_content(event.text):
                db_user = data.get("db_user")
                lang = db_user.language if db_user else "uz"
                await event.answer(t(lang, "adult_content_warning"))
                return None

        return await handler(event, data)
