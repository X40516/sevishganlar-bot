"""
🎲 Juftlik o'yinlari bo'limi: bilish testi, kim ko'proq, haqiqat/tanlov, moslik testi, viktorina.
"""
import random

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import (
    add_game_answer,
    complete_game,
    create_game,
    get_active_game,
    get_couple_for_user,
    get_game_by_id,
    get_partner_user,
    get_user_by_id,
    update_game_payload,
)
from handlers.states import GameStates
from services.content import COMPAT_QUESTIONS, PARTNER_QUESTIONS, QUIZ_QUESTIONS, TRUTH_PROMPTS, DARE_PROMPTS, WHO_MORE_STATEMENTS
from utils.helpers import home_button

router = Router(name="games")


def _games_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❤️ Bir-biringizni qanchalik bilasiz?", callback_data="game:know_start")],
            [InlineKeyboardButton(text="😂 Kim ko'proq?", callback_data="game:who_start")],
            [InlineKeyboardButton(text="💭 Haqiqat yoki tanlov", callback_data="game:truth_dare_menu")],
            [InlineKeyboardButton(text="🔥 Moslik testi", callback_data="game:compat_start")],
            [InlineKeyboardButton(text="🧠 Juftlik viktorinasi", callback_data="game:quiz_start")],
            [home_button()],
        ]
    )


@router.message(F.text.in_({"🎲 Juftlik o'yini", "🎲 Juftlik o'yinlari"}))
async def games_menu(message: Message, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer("❌ Avval juftingiz bilan ulanishingiz kerak.")
        return
    await message.answer("🎲 O'yinlardan birini tanlang:", reply_markup=_games_menu_kb())


# ================== 1) Bir-biringizni qanchalik bilasiz ==================

@router.callback_query(F.data == "game:know_start")
async def game_know_start(callback: CallbackQuery, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌ Juftlik topilmadi.", show_alert=True)
        return

    game = await get_active_game(session, couple.id, "know")
    if game is None:
        questions = random.sample(PARTNER_QUESTIONS, k=min(5, len(PARTNER_QUESTIONS)))
        game = await create_game(session, couple.id, "know", {"questions": questions, "answers": {}, "idx": {}, "done": []})

    await state.set_state(GameStates.know_answering)
    await state.update_data(game_id=game.id)

    user_key = str(db_user.id)
    idx = game.payload["idx"].get(user_key, 0)
    questions = game.payload["questions"]
    if idx >= len(questions):
        await callback.message.answer("✅ Siz allaqachon barcha savollarga javob berdingiz. Juftingizni kutmoqdamiz.")
        await callback.answer()
        return

    await callback.message.answer(f"❤️ {idx + 1}-savol: {questions[idx]}")
    await callback.answer()


@router.message(GameStates.know_answering, F.text)
async def game_know_answer(message: Message, state: FSMContext, session: AsyncSession, db_user: User) -> None:
    data = await state.get_data()
    game_id = data.get("game_id")
    game = await get_game_by_id(session, game_id) if game_id else None
    if game is None or game.status != "in_progress":
        await state.clear()
        await message.answer("❌ O'yin sessiyasi topilmadi. Qaytadan boshlang.")
        return

    payload = game.payload
    user_key = str(db_user.id)
    idx = payload["idx"].get(user_key, 0)
    questions = payload["questions"]

    payload.setdefault("answers", {}).setdefault(user_key, [])
    payload["answers"][user_key].append(message.text)
    idx += 1
    payload["idx"][user_key] = idx

    await add_game_answer(session, game.id, db_user.id, idx - 1, message.text)

    if idx < len(questions):
        await update_game_payload(session, game, payload)
        await message.answer(f"❤️ {idx + 1}-savol: {questions[idx]}")
        return

    payload.setdefault("done", [])
    if db_user.id not in payload["done"]:
        payload["done"].append(db_user.id)
    await update_game_payload(session, game, payload)
    await state.clear()

    couple = await get_couple_for_user(session, db_user.id)
    partner = await get_partner_user(session, couple, db_user.id) if couple else None

    if partner and partner.id in payload["done"]:
        answers_a = payload["answers"].get(str(db_user.id), [])
        answers_b = payload["answers"].get(str(partner.id), [])
        matches = sum(
            1 for a, b in zip(answers_a, answers_b) if a.strip().lower() == b.strip().lower()
        )
        total = len(questions)
        percent = round(matches / total * 100)
        await complete_game(session, game)
        result_text = f"❤️ Natija:\n{total} ta savoldan {matches} tasi mos keldi!\nMoslik: {percent}%"
        await message.answer(result_text)
        try:
            await message.bot.send_message(partner.telegram_id, result_text)
        except Exception:
            pass
    else:
        await message.answer("✅ Javoblaringiz saqlandi! Juftingiz javob berishini kutmoqdamiz. 💭")


# ================== 2) Kim ko'proq ==================

@router.callback_query(F.data == "game:who_start")
async def game_who_start(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌ Juftlik topilmadi.", show_alert=True)
        return

    partner = await get_partner_user(session, couple, db_user.id)
    if partner is None:
        await callback.answer("❌ Partner topilmadi.", show_alert=True)
        return

    statement = random.choice(WHO_MORE_STATEMENTS)
    game = await create_game(session, couple.id, "who", {"statement": statement, "choices": {}})

    kb_for = lambda me, other: InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"👤 {me.full_name}", callback_data=f"game:who_vote:{game.id}:{me.id}"),
                InlineKeyboardButton(text=f"❤️ {other.full_name}", callback_data=f"game:who_vote:{game.id}:{other.id}"),
            ]
        ]
    )

    await callback.message.answer(f"😂 {statement}", reply_markup=kb_for(db_user, partner))
    try:
        await callback.bot.send_message(
            partner.telegram_id, f"😂 {statement}", reply_markup=kb_for(partner, db_user)
        )
    except Exception:
        pass
    await callback.answer()


@router.callback_query(F.data.startswith("game:who_vote:"))
async def game_who_vote(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    _, _, game_id_str, target_id_str = callback.data.split(":")
    game = await get_game_by_id(session, int(game_id_str))
    if game is None or game.status != "in_progress":
        await callback.answer("❌ O'yin muddati o'tgan.", show_alert=True)
        return

    payload = game.payload
    payload.setdefault("choices", {})[str(db_user.id)] = int(target_id_str)
    await update_game_payload(session, game, payload)

    await callback.message.edit_text(f"😂 {payload['statement']}\n\n✅ Ovozingiz qabul qilindi. Juftingizni kutmoqdamiz...")
    await callback.answer()

    couple = await get_couple_for_user(session, db_user.id)
    partner = await get_partner_user(session, couple, db_user.id) if couple else None
    if partner and str(partner.id) in payload["choices"]:
        choice_self = payload["choices"][str(db_user.id)]
        choice_partner = payload["choices"][str(partner.id)]
        await complete_game(session, game)

        if choice_self == choice_partner:
            target_user = await get_user_by_id(session, choice_self)
            result_text = f"😂 Ikkalangiz ham bir xil fikrdasiz! {target_user.full_name} ko'proq shunday!"
        else:
            self_target = await get_user_by_id(session, choice_self)
            partner_target = await get_user_by_id(session, choice_partner)
            result_text = (
                f"😂 Bu safar fikringiz turlicha!\n"
                f"👤 {db_user.full_name}: {self_target.full_name}\n"
                f"❤️ {partner.full_name}: {partner_target.full_name}"
            )

        await callback.message.answer(result_text)
        try:
            await callback.bot.send_message(partner.telegram_id, result_text)
        except Exception:
            pass


# ================== 3) Haqiqat yoki tanlov ==================

@router.callback_query(F.data == "game:truth_dare_menu")
async def game_truth_dare_menu(callback: CallbackQuery) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Haqiqat", callback_data="game:truth")],
            [InlineKeyboardButton(text="🎯 Tanlov", callback_data="game:dare")],
            [home_button()],
        ]
    )
    await callback.message.edit_text("💭 Tanlang:", reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "game:truth")
async def game_truth(callback: CallbackQuery) -> None:
    prompt = random.choice(TRUTH_PROMPTS)
    await callback.message.answer(f"💬 Savolingiz:\n{prompt}\n\nJavobingizni juftingizga '💌 Xat yuborish' orqali yuboring.")
    await callback.answer()


@router.callback_query(F.data == "game:dare")
async def game_dare(callback: CallbackQuery) -> None:
    prompt = random.choice(DARE_PROMPTS)
    await callback.message.answer(f"🎯 Vazifangiz:\n{prompt}")
    await callback.answer()


# ================== 4) Moslik testi va 5) Juftlik viktorinasi (umumiy MCQ mexanizmi) ==================

def _mcq_keyboard(game_id: int, q_index: int, options: list[str]) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=opt, callback_data=f"game:ans:{game_id}:{q_index}:{i}")] for i, opt in enumerate(options)]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def _start_mcq_game(callback: CallbackQuery, session: AsyncSession, db_user: User, game_type: str, intro: str) -> None:
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await callback.answer("❌ Juftlik topilmadi.", show_alert=True)
        return

    game = await get_active_game(session, couple.id, game_type)
    if game is None:
        game = await create_game(session, couple.id, game_type, {"answers": {}, "idx": {}, "done": []})

    user_key = str(db_user.id)
    idx = game.payload["idx"].get(user_key, 0)

    pool = COMPAT_QUESTIONS if game_type == "compat" else QUIZ_QUESTIONS
    if idx >= len(pool):
        await callback.message.answer("✅ Siz allaqachon javob berdingiz. Juftingizni kutmoqdamiz.")
        await callback.answer()
        return

    if game_type == "compat":
        question_text, options = pool[idx]
    else:
        question_text, opts_with_flag = pool[idx]
        options = [o[0] for o in opts_with_flag]

    await callback.message.answer(
        f"{intro}\n\n{idx + 1}-savol: {question_text}", reply_markup=_mcq_keyboard(game.id, idx, options)
    )
    await callback.answer()


@router.callback_query(F.data == "game:compat_start")
async def game_compat_start(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await _start_mcq_game(callback, session, db_user, "compat", "🔥 Moslik testi boshlandi!")


@router.callback_query(F.data == "game:quiz_start")
async def game_quiz_start(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await _start_mcq_game(callback, session, db_user, "quiz", "🧠 Juftlik viktorinasi boshlandi!")


@router.callback_query(F.data.startswith("game:ans:"))
async def game_mcq_answer(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    _, _, game_id_str, q_index_str, opt_index_str = callback.data.split(":")
    game_id = int(game_id_str)
    q_index = int(q_index_str)
    opt_index = int(opt_index_str)

    game = await get_game_by_id(session, game_id)
    if game is None or game.status != "in_progress":
        await callback.answer("❌ O'yin muddati o'tgan.", show_alert=True)
        return

    payload = game.payload
    user_key = str(db_user.id)
    current_idx = payload["idx"].get(user_key, 0)
    if q_index != current_idx:
        await callback.answer()
        return

    pool = COMPAT_QUESTIONS if game.game_type == "compat" else QUIZ_QUESTIONS

    payload.setdefault("answers", {}).setdefault(user_key, [])
    payload["answers"][user_key].append(opt_index)

    is_correct = None
    if game.game_type == "quiz":
        _, opts_with_flag = pool[q_index]
        is_correct = opts_with_flag[opt_index][1]

    next_idx = q_index + 1
    payload["idx"][user_key] = next_idx
    await update_game_payload(session, game, payload)

    feedback = ""
    if is_correct is not None:
        feedback = "✅ To'g'ri!\n\n" if is_correct else "❌ Unchalik emas.\n\n"

    if next_idx < len(pool):
        if game.game_type == "compat":
            question_text, options = pool[next_idx]
        else:
            question_text, opts_with_flag = pool[next_idx]
            options = [o[0] for o in opts_with_flag]
        await callback.message.edit_text(
            f"{feedback}{next_idx + 1}-savol: {question_text}", reply_markup=_mcq_keyboard(game.id, next_idx, options)
        )
        await callback.answer()
        return

    payload.setdefault("done", [])
    if db_user.id not in payload["done"]:
        payload["done"].append(db_user.id)
    await update_game_payload(session, game, payload)
    await callback.message.edit_text(f"{feedback}✅ Siz barcha savollarga javob berdingiz. Juftingizni kutmoqdamiz...")
    await callback.answer()

    couple = await get_couple_for_user(session, db_user.id)
    partner = await get_partner_user(session, couple, db_user.id) if couple else None
    if not partner or partner.id not in payload["done"]:
        return

    await complete_game(session, game)
    answers_a = payload["answers"].get(str(db_user.id), [])
    answers_b = payload["answers"].get(str(partner.id), [])

    if game.game_type == "compat":
        matches = sum(1 for a, b in zip(answers_a, answers_b) if a == b)
        percent = round(matches / len(pool) * 100)
        result_text = f"🔥 Moslik: {percent}%\n\nBu natija faqat o'yin uchun 😊"
    else:
        score_a = sum(1 for i, a in enumerate(answers_a) if pool[i][1][a][1])
        score_b = sum(1 for i, b in enumerate(answers_b) if pool[i][1][b][1])
        result_text = (
            f"🏁 Viktorina tugadi!\n\n"
            f"👤 {db_user.full_name}: {score_a}/{len(pool)}\n"
            f"❤️ {partner.full_name}: {score_b}/{len(pool)}"
        )

    await callback.message.answer(result_text)
    try:
        await callback.bot.send_message(partner.telegram_id, result_text)
    except Exception:
        pass
