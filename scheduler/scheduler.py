"""
Kunlik avtomatik xabarlar (APScheduler).
"""
import logging
import random
from datetime import date

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import DAILY_MESSAGE_HOUR, DAILY_QUESTION_HOUR
from database.database import async_session
from database.queries import get_all_user_telegram_ids, get_couples_with_users, get_answer_for_today
from services.content import DAILY_ROMANTIC_MESSAGES

logger = logging.getLogger(__name__)


async def job_daily_question_reminder(bot: Bot) -> None:
    async with async_session() as session:
        couples = await get_couples_with_users(session)
        today = date.today()
        for couple, u1, u2 in couples:
            for user in (u1, u2):
                answer = await get_answer_for_today(session, couple.id, user.id, today)
                if answer is not None:
                    continue
                try:
                    from database.queries import get_notification_settings

                    settings = await get_notification_settings(session, user.id)
                    if not settings.daily_question:
                        continue
                    await bot.send_message(
                        user.telegram_id,
                        "💭 Bugungi savolga javob berishni unutmang! Asosiy menyudan "
                        "'💭 Bugungi savol' tugmasini bosing.",
                    )
                except Exception:
                    logger.warning("Kunlik savol eslatmasini yuborib bo'lmadi: %s", user.telegram_id)


async def job_daily_romantic_message(bot: Bot) -> None:
    async with async_session() as session:
        telegram_ids = await get_all_user_telegram_ids(session, notif_field="daily_message")
        message_text = random.choice(DAILY_ROMANTIC_MESSAGES)
        for tg_id in telegram_ids:
            try:
                await bot.send_message(tg_id, message_text)
            except Exception:
                logger.warning("Kunlik romantik xabarni yuborib bo'lmadi: %s", tg_id)


def setup_scheduler(scheduler: AsyncIOScheduler, bot: Bot) -> None:
    scheduler.add_job(job_daily_question_reminder, "cron", hour=DAILY_QUESTION_HOUR, minute=0, args=[bot])
    scheduler.add_job(job_daily_romantic_message, "cron", hour=DAILY_MESSAGE_HOUR, minute=0, args=[bot])
