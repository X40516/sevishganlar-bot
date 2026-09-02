"""
Barcha database CRUD operatsiyalari.
"""
import secrets
import string
from datetime import date, datetime

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    AdminLog,
    Couple,
    DailyQuestion,
    Game,
    GameAnswer,
    Gift,
    GiftTransaction,
    Letter,
    Memory,
    NotificationSettings,
    PairInvite,
    QuestionAnswer,
    User,
)
from services.content import DAILY_QUESTIONS, GIFTS


# ---------- Foydalanuvchilar ----------

async def get_or_create_user(session: AsyncSession, telegram_id: int, full_name: str, username: str | None) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(telegram_id=telegram_id, full_name=full_name, username=username)
        session.add(user)
        await session.flush()
        session.add(NotificationSettings(user_id=user.id))
        await session.commit()
        await session.refresh(user)
    else:
        changed = False
        if user.full_name != full_name:
            user.full_name = full_name
            changed = True
        if user.username != username:
            user.username = username
            changed = True
        if changed:
            await session.commit()
    return user


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def set_user_ban(session: AsyncSession, user_id: int, banned: bool) -> None:
    await session.execute(update(User).where(User.id == user_id).values(is_banned=banned))
    await session.commit()


# ---------- Bildirishnomalar ----------

async def get_notification_settings(session: AsyncSession, user_id: int) -> NotificationSettings:
    result = await session.execute(select(NotificationSettings).where(NotificationSettings.user_id == user_id))
    settings = result.scalar_one_or_none()
    if settings is None:
        settings = NotificationSettings(user_id=user_id)
        session.add(settings)
        await session.commit()
        await session.refresh(settings)
    return settings


async def toggle_notification(session: AsyncSession, user_id: int, field: str) -> NotificationSettings:
    settings = await get_notification_settings(session, user_id)
    current = getattr(settings, field)
    setattr(settings, field, not current)
    await session.commit()
    await session.refresh(settings)
    return settings


# ---------- Juftlik taklifi (pairing) ----------

def _generate_code(length: int = 8) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


async def create_pair_invite(session: AsyncSession, inviter_id: int) -> PairInvite:
    code = _generate_code()
    result = await session.execute(select(PairInvite).where(PairInvite.code == code))
    while result.scalar_one_or_none() is not None:
        code = _generate_code()
        result = await session.execute(select(PairInvite).where(PairInvite.code == code))

    invite = PairInvite(code=code, inviter_id=inviter_id)
    session.add(invite)
    await session.commit()
    await session.refresh(invite)
    return invite


async def get_invite_by_code(session: AsyncSession, code: str) -> PairInvite | None:
    result = await session.execute(select(PairInvite).where(PairInvite.code == code, PairInvite.used.is_(False)))
    return result.scalar_one_or_none()


async def mark_invite_used(session: AsyncSession, invite: PairInvite) -> None:
    invite.used = True
    await session.commit()


# ---------- Juftliklar ----------

async def create_couple(session: AsyncSession, user1_id: int, user2_id: int) -> Couple:
    couple = Couple(user1_id=user1_id, user2_id=user2_id)
    session.add(couple)
    await session.commit()
    await session.refresh(couple)
    return couple


async def get_couple_for_user(session: AsyncSession, user_id: int) -> Couple | None:
    result = await session.execute(
        select(Couple).where(
            Couple.is_active.is_(True),
            ((Couple.user1_id == user_id) | (Couple.user2_id == user_id)),
        )
    )
    return result.scalar_one_or_none()


async def get_partner_user(session: AsyncSession, couple: Couple, self_user_id: int) -> User | None:
    partner_id = couple.user2_id if couple.user1_id == self_user_id else couple.user1_id
    return await get_user_by_id(session, partner_id)


async def set_anniversary_date(session: AsyncSession, couple_id: int, when: date) -> None:
    await session.execute(update(Couple).where(Couple.id == couple_id).values(anniversary_date=when))
    await session.commit()


async def deactivate_couple(session: AsyncSession, couple_id: int) -> None:
    await session.execute(update(Couple).where(Couple.id == couple_id).values(is_active=False))
    await session.commit()


# ---------- Xatlar ----------

async def create_letter(
    session: AsyncSession,
    couple_id: int,
    sender_id: int,
    letter_type: str,
    content: str = "",
    photo_file_id: str | None = None,
) -> Letter:
    letter = Letter(
        couple_id=couple_id,
        sender_id=sender_id,
        letter_type=letter_type,
        content=content,
        photo_file_id=photo_file_id,
    )
    session.add(letter)
    await session.commit()
    await session.refresh(letter)
    return letter


# ---------- Kunlik savol ----------

async def seed_daily_questions(session: AsyncSession) -> None:
    result = await session.execute(select(func.count()).select_from(DailyQuestion))
    count = result.scalar_one()
    if count == 0:
        for text in DAILY_QUESTIONS:
            session.add(DailyQuestion(text=text))
        await session.commit()


async def get_all_daily_questions(session: AsyncSession) -> list[DailyQuestion]:
    result = await session.execute(select(DailyQuestion).order_by(DailyQuestion.id))
    return list(result.scalars().all())


async def add_daily_question(session: AsyncSession, text: str) -> DailyQuestion:
    question = DailyQuestion(text=text)
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


async def get_todays_question(session: AsyncSession, couple_id: int, for_date: date) -> DailyQuestion:
    questions = await get_all_daily_questions(session)
    index = hash((couple_id, for_date.isoformat())) % len(questions)
    return questions[index]


async def get_answer_for_today(
    session: AsyncSession, couple_id: int, user_id: int, for_date: date
) -> QuestionAnswer | None:
    result = await session.execute(
        select(QuestionAnswer).where(
            QuestionAnswer.couple_id == couple_id,
            QuestionAnswer.user_id == user_id,
            QuestionAnswer.answer_date == for_date,
        )
    )
    return result.scalar_one_or_none()


async def save_question_answer(
    session: AsyncSession,
    couple_id: int,
    user_id: int,
    question: DailyQuestion,
    for_date: date,
    answer_text: str,
) -> QuestionAnswer:
    existing = await get_answer_for_today(session, couple_id, user_id, for_date)
    if existing:
        existing.answer_text = answer_text
        await session.commit()
        await session.refresh(existing)
        return existing

    answer = QuestionAnswer(
        couple_id=couple_id,
        user_id=user_id,
        question_id=question.id,
        answer_date=for_date,
        question_text=question.text,
        answer_text=answer_text,
    )
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return answer


# ---------- O'yinlar ----------

async def create_game(session: AsyncSession, couple_id: int, game_type: str, payload: dict) -> Game:
    game = Game(couple_id=couple_id, game_type=game_type, payload=payload)
    session.add(game)
    await session.commit()
    await session.refresh(game)
    return game


async def get_active_game(session: AsyncSession, couple_id: int, game_type: str) -> Game | None:
    result = await session.execute(
        select(Game).where(
            Game.couple_id == couple_id,
            Game.game_type == game_type,
            Game.status == "in_progress",
        )
    )
    return result.scalar_one_or_none()


async def get_game_by_id(session: AsyncSession, game_id: int) -> Game | None:
    result = await session.execute(select(Game).where(Game.id == game_id))
    return result.scalar_one_or_none()


async def update_game_payload(session: AsyncSession, game: Game, payload: dict) -> None:
    game.payload = payload
    await session.commit()


async def complete_game(session: AsyncSession, game: Game) -> None:
    game.status = "completed"
    await session.commit()


async def add_game_answer(session: AsyncSession, game_id: int, user_id: int, question_index: int, answer_text: str) -> None:
    session.add(GameAnswer(game_id=game_id, user_id=user_id, question_index=question_index, answer_text=answer_text))
    await session.commit()


# ---------- Sovg'alar ----------

async def seed_gifts(session: AsyncSession) -> None:
    result = await session.execute(select(func.count()).select_from(Gift))
    count = result.scalar_one()
    if count == 0:
        for name, emoji in GIFTS:
            session.add(Gift(name=name, emoji=emoji))
        await session.commit()


async def get_all_gifts(session: AsyncSession) -> list[Gift]:
    result = await session.execute(select(Gift).order_by(Gift.id))
    return list(result.scalars().all())


async def get_gift_by_id(session: AsyncSession, gift_id: int) -> Gift | None:
    result = await session.execute(select(Gift).where(Gift.id == gift_id))
    return result.scalar_one_or_none()


async def create_gift_transaction(session: AsyncSession, couple_id: int, sender_id: int, gift_id: int) -> None:
    session.add(GiftTransaction(couple_id=couple_id, sender_id=sender_id, gift_id=gift_id))
    await session.commit()


async def get_gift_stats(session: AsyncSession) -> list[tuple[str, str, int]]:
    result = await session.execute(
        select(Gift.name, Gift.emoji, func.count(GiftTransaction.id))
        .outerjoin(GiftTransaction, GiftTransaction.gift_id == Gift.id)
        .group_by(Gift.id)
        .order_by(Gift.id)
    )
    return [(row[0], row[1], row[2]) for row in result.all()]


# ---------- Xotiralar ----------

async def add_memory(
    session: AsyncSession, couple_id: int, user_id: int, photo_file_id: str, caption: str, memory_date: date
) -> Memory:
    memory = Memory(couple_id=couple_id, user_id=user_id, photo_file_id=photo_file_id, caption=caption, memory_date=memory_date)
    session.add(memory)
    await session.commit()
    await session.refresh(memory)
    return memory


async def get_memories(session: AsyncSession, couple_id: int) -> list[Memory]:
    result = await session.execute(
        select(Memory).where(Memory.couple_id == couple_id).order_by(Memory.memory_date.desc(), Memory.id.desc())
    )
    return list(result.scalars().all())


async def get_memory_by_id(session: AsyncSession, memory_id: int) -> Memory | None:
    result = await session.execute(select(Memory).where(Memory.id == memory_id))
    return result.scalar_one_or_none()


async def delete_memory(session: AsyncSession, memory_id: int) -> None:
    memory = await get_memory_by_id(session, memory_id)
    if memory:
        await session.delete(memory)
        await session.commit()


# ---------- Admin ----------

async def log_admin_action(session: AsyncSession, admin_id: int, action: str, details: str = "") -> None:
    session.add(AdminLog(admin_id=admin_id, action=action, details=details))
    await session.commit()


async def get_stats(session: AsyncSession) -> dict:
    total_users = (await session.execute(select(func.count()).select_from(User))).scalar_one()
    total_couples = (
        await session.execute(select(func.count()).select_from(Couple).where(Couple.is_active.is_(True)))
    ).scalar_one()
    today = datetime.utcnow().date()
    week_ago = today.toordinal() - 7
    month_ago = today.toordinal() - 30

    weekly_new = (
        await session.execute(
            select(func.count()).select_from(User).where(func.date(User.created_at) >= date.fromordinal(week_ago))
        )
    ).scalar_one()
    monthly_new = (
        await session.execute(
            select(func.count()).select_from(User).where(func.date(User.created_at) >= date.fromordinal(month_ago))
        )
    ).scalar_one()
    active_today = (
        await session.execute(
            select(func.count(func.distinct(QuestionAnswer.user_id))).where(QuestionAnswer.answer_date == today)
        )
    ).scalar_one()
    total_letters = (await session.execute(select(func.count()).select_from(Letter))).scalar_one()
    total_gifts = (await session.execute(select(func.count()).select_from(GiftTransaction))).scalar_one()
    total_memories = (await session.execute(select(func.count()).select_from(Memory))).scalar_one()

    return {
        "total_users": total_users,
        "total_couples": total_couples,
        "active_today": active_today,
        "weekly_new": weekly_new,
        "monthly_new": monthly_new,
        "total_letters": total_letters,
        "total_gifts": total_gifts,
        "total_memories": total_memories,
    }


async def get_latest_users(session: AsyncSession, limit: int = 10) -> list[User]:
    result = await session.execute(select(User).order_by(User.created_at.desc()).limit(limit))
    return list(result.scalars().all())


async def get_latest_couples(session: AsyncSession, limit: int = 10) -> list[Couple]:
    result = await session.execute(
        select(Couple).where(Couple.is_active.is_(True)).order_by(Couple.created_at.desc()).limit(limit)
    )
    return list(result.scalars().all())


async def get_all_user_telegram_ids(session: AsyncSession, notif_field: str | None = None) -> list[int]:
    if notif_field is None:
        result = await session.execute(select(User.telegram_id).where(User.is_banned.is_(False)))
        return [row[0] for row in result.all()]

    result = await session.execute(
        select(User.telegram_id)
        .join(NotificationSettings, NotificationSettings.user_id == User.id)
        .where(User.is_banned.is_(False), getattr(NotificationSettings, notif_field).is_(True))
    )
    return [row[0] for row in result.all()]


async def get_couples_with_users(session: AsyncSession) -> list[tuple[Couple, User, User]]:
    couples = await session.execute(select(Couple).where(Couple.is_active.is_(True)))
    result: list[tuple[Couple, User, User]] = []
    for couple in couples.scalars().all():
        u1 = await get_user_by_id(session, couple.user1_id)
        u2 = await get_user_by_id(session, couple.user2_id)
        if u1 and u2:
            result.append((couple, u1, u2))
    return result
