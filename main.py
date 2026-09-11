"""
@JuftimBotbot - sevishgan juftliklar uchun Telegram bot.
Asosiy ishga tushirish fayli.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN
from database.database import async_session, init_db
from database.queries import seed_daily_questions, seed_gifts
from handlers import admin, couple, days, games, gifts, letters, memories, music, questions, settings, start, support
from middlewares.content_filter import AdultContentMiddleware
from middlewares.db import DBSessionMiddleware
from middlewares.user import UserMiddleware
from scheduler.scheduler import setup_scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    await init_db()
    async with async_session() as session:
        await seed_daily_questions(session)
        await seed_gifts(session)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.update.outer_middleware.register(DBSessionMiddleware())
    dp.update.outer_middleware.register(UserMiddleware())
    dp.update.outer_middleware.register(AdultContentMiddleware())

    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(couple.router)
    dp.include_router(letters.router)
    dp.include_router(music.router)
    dp.include_router(games.router)
    dp.include_router(questions.router)
    dp.include_router(gifts.router)
    dp.include_router(memories.router)
    dp.include_router(days.router)
    dp.include_router(settings.router)
    dp.include_router(support.router)

    scheduler = AsyncIOScheduler()
    setup_scheduler(scheduler, bot)
    scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    me = await bot.get_me()
    logger.info("Bot ishga tushdi: @%s", me.username)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
