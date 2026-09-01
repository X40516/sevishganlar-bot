"""
Sevishganlar (juftliklar) uchun maxsus Telegram bot
- Bir-biriga ulanish (pairing) kod orqali
- Sevgi xabari / kompliment yuborish
- Romantik iqtiboslar
- Uchrashuv g'oyalari
- Yodgorlik sanasi va "necha kun birgamiz" hisoblagichi
- 18+ yosh tasdiqlash
- Erkin suhbat (faqat sevgi mavzusida, 18+ tasdiqlangandan keyin)
- Sevgi testi (viktorina)

Ishga tushirish:
    1. .env faylida BOT_TOKEN ni to'ldiring
    2. pip install -r requirements.txt
    3. python bot.py
"""

import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import lovers
import love_chat
import quiz

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Menyular ----------

AGE_GATE_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("✅ Ha, men 18 yoshdan kattaman", callback_data="age_yes")],
        [InlineKeyboardButton("❌ Yo'q", callback_data="age_no")],
    ]
)

LOVERS_MENU = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("💌 Sevgi xabari", callback_data="love_msg"),
            InlineKeyboardButton("😊 Kompliment", callback_data="love_compliment"),
        ],
        [
            InlineKeyboardButton("📜 Iqtibos", callback_data="love_quote"),
            InlineKeyboardButton("🎲 Uchrashuv g'oyasi", callback_data="love_dateidea"),
        ],
        [
            InlineKeyboardButton("🔗 Ulanish kodim", callback_data="love_mycode"),
            InlineKeyboardButton("💑 Necha kun birgamiz", callback_data="love_together"),
        ],
        [
            InlineKeyboardButton("👤 Partnyorim", callback_data="love_partner"),
            InlineKeyboardButton("❌ Ajralish", callback_data="love_unpair"),
        ],
        [
            InlineKeyboardButton("💬 Erkin suhbat", callback_data="love_freechat"),
        ],
        [
            InlineKeyboardButton("🎮 Sevgi testi", callback_data="quiz_start"),
        ],
    ]
)


# ---------- /start va /help ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lovers.get_or_create_user(user_id)

    if not lovers.is_adult(user_id):
        await update.message.reply_text(
            "💕 Salom! Men sevishganlar uchun maxsus botman.\n\n"
            "🔞 Botdan foydalanishdan oldin yoshingizni tasdiqlang:",
            reply_markup=AGE_GATE_KEYBOARD,
        )
        return

    await show_menu(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "💕 Sevishganlar boti buyruqlari:\n\n"
        "/start - Botni boshlash\n"
        "/menu - Asosiy menyuni ko'rsatish\n"
        "/pair <kod> - Partneringiz bilan ulanish\n"
        "/anniversary YYYY-MM-DD - Yodgorlik sanasini kiritish\n"
        "/help - Yordam"
    )
    await update.message.reply_text(text)


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "💕 Sevishganlar menyusi — kerakli bo'limni tanlang:",
        reply_markup=LOVERS_MENU,
    )


# ---------- Yosh tasdiqlash ----------

async def age_gate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lovers.get_or_create_user(user_id)

    if query.data == "age_yes":
        lovers.confirm_adult(user_id)
        await query.message.reply_text(
            "Rahmat! 💕 Sevishganlar menyusi ochildi:",
            reply_markup=LOVERS_MENU,
        )
    else:
        await query.message.reply_text(
            "Tushunarli. Bu bot faqat 18 yoshdan katta foydalanuvchilar uchun mavjud."
        )


# ---------- Buyruqlar ----------

async def pair_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanish: /pair <kod>"""
    user_id = update.effective_user.id
    lovers.get_or_create_user(user_id)

    if not lovers.is_adult(user_id):
        await update.message.reply_text(
            "🔞 Bu funksiya faqat 18 yoshdan katta foydalanuvchilar uchun. /start orqali yoshingizni tasdiqlang."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Foydalanish: /pair <kod>\nPartneringizning ulanish kodini kiriting."
        )
        return

    code = context.args[0]
    partner_uid = lovers.find_user_by_code(code)
    if not partner_uid:
        await update.message.reply_text("Bunday kod topilmadi. Kodni tekshirib qaytadan urinib ko'ring.")
        return

    if not lovers.is_adult(int(partner_uid)):
        await update.message.reply_text(
            "Partneringiz hali 18+ tasdiqlamagan. Ikkalangiz ham yoshni tasdiqlashingiz kerak."
        )
        return

    success = lovers.pair_users(user_id, partner_uid)
    if success:
        await update.message.reply_text("💞 Muvaffaqiyatli ulandingiz! Endi bir-biringizga sevgi xabarlari yubora olasiz.")
        try:
            await context.bot.send_message(
                chat_id=int(partner_uid),
                text="💞 Sizning partneringiz ulandi! Endi bir-biringizga sevgi xabarlari yubora olasiz.",
            )
        except Exception:
            logger.warning("Partnyorga xabar yuborib bo'lmadi: %s", partner_uid)
    else:
        await update.message.reply_text("Ulanishda xatolik yuz berdi. O'zingizning kodingizni kiritmaganingizga ishonch hosil qiling.")


async def anniversary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Foydalanish: /anniversary YYYY-MM-DD"""
    user_id = update.effective_user.id
    lovers.get_or_create_user(user_id)

    if not lovers.is_adult(user_id):
        await update.message.reply_text(
            "🔞 Bu funksiya faqat 18 yoshdan katta foydalanuvchilar uchun. /start orqali yoshingizni tasdiqlang."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "Foydalanish: /anniversary YYYY-MM-DD\nMasalan: /anniversary 2023-05-01"
        )
        return

    date_str = context.args[0]
    if lovers.set_anniversary(user_id, date_str):
        await update.message.reply_text(f"✅ Yodgorlik sanangiz saqlandi: {date_str}")
    else:
        await update.message.reply_text("Sana formati noto'g'ri. YYYY-MM-DD formatida kiriting (masalan: 2023-05-01).")


# ---------- Sevishganlar menyusi tugmalari ----------

async def lovers_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lovers.get_or_create_user(user_id)

    if not lovers.is_adult(user_id):
        await query.message.reply_text(
            "🔞 Bu bot faqat 18 yoshdan katta foydalanuvchilar uchun.",
            reply_markup=AGE_GATE_KEYBOARD,
        )
        return

    action = query.data

    if action in ("love_msg", "love_compliment"):
        partner_id = lovers.get_partner_id(user_id)
        if not partner_id:
            await query.message.reply_text(
                "Hali hech kim bilan ulanmagansiz. Avval /pair <kod> orqali ulaning yoki 'Ulanish kodim' tugmasini bosing."
            )
            return
        text = lovers.random_love_message() if action == "love_msg" else lovers.random_compliment()
        try:
            await context.bot.send_message(chat_id=int(partner_id), text=f"💌 Sizga xabar bor:\n\n{text}")
            await query.message.reply_text("✅ Xabaringiz yuborildi!")
        except Exception:
            await query.message.reply_text("Xabar yuborib bo'lmadi. Partnyoringiz botni bloklagan bo'lishi mumkin.")

    elif action == "love_quote":
        await query.message.reply_text(lovers.random_quote())

    elif action == "love_dateidea":
        await query.message.reply_text(f"Bugungi g'oya:\n\n{lovers.random_date_idea()}")

    elif action == "love_mycode":
        info = lovers.get_or_create_user(user_id)
        await query.message.reply_text(
            f"Sizning ulanish kodingiz: `{info['code']}`\n\n"
            "Buni partneringizga yuboring, u esa /pair " + info["code"] + " buyrug'ini yozsin.",
            parse_mode="Markdown",
        )

    elif action == "love_together":
        anniversary = lovers.get_anniversary(user_id)
        if not anniversary:
            await query.message.reply_text(
                "Yodgorlik sanangiz kiritilmagan. /anniversary YYYY-MM-DD orqali kiriting."
            )
            return
        days = lovers.days_together(anniversary)
        await query.message.reply_text(f"💑 Siz {anniversary} dan buyon birgasiz — jami {days} kun! 🎉")

    elif action == "love_partner":
        partner_id = lovers.get_partner_id(user_id)
        if not partner_id:
            await query.message.reply_text("Hali hech kim bilan ulanmagansiz.")
        else:
            await query.message.reply_text("💑 Siz allaqachon partneringiz bilan ulangansiz.")

    elif action == "love_freechat":
        await query.message.reply_text(
            "💬 Sevgi haqida menga xohlagan narsangizni yozing — tinglayman 😊"
        )

    elif action == "love_unpair":
        lovers.unpair_user(user_id)
        await query.message.reply_text("Ulanish bekor qilindi.")


# ---------- Erkin suhbat (faqat sevgi mavzusida) ----------

async def free_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lovers.get_or_create_user(user_id)

    if not lovers.is_adult(user_id):
        await update.message.reply_text(
            "🔞 Bu bot faqat 18 yoshdan katta foydalanuvchilar uchun.",
            reply_markup=AGE_GATE_KEYBOARD,
        )
        return

    reply = love_chat.get_response(update.message.text)
    await update.message.reply_text(reply)


# ---------- Sevgi testi (viktorina) ----------

def build_question_keyboard(q_index: int) -> InlineKeyboardMarkup:
    question = quiz.QUESTIONS[q_index]
    buttons = [
        [InlineKeyboardButton(text, callback_data=f"quiz_ans_{q_index}_{i}")]
        for i, (text, _correct) in enumerate(question["options"])
    ]
    return InlineKeyboardMarkup(buttons)


async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lovers.get_or_create_user(user_id)

    if not lovers.is_adult(user_id):
        await query.message.reply_text(
            "🔞 Bu bot faqat 18 yoshdan katta foydalanuvchilar uchun.",
            reply_markup=AGE_GATE_KEYBOARD,
        )
        return

    data = query.data

    if data == "quiz_start":
        context.user_data["quiz_score"] = 0
        context.user_data["quiz_index"] = 0
        question = quiz.QUESTIONS[0]
        await query.message.reply_text(
            f"🎮 Sevgi testi boshlandi!\n\n1-savol: {question['question']}",
            reply_markup=build_question_keyboard(0),
        )
        return

    # data format: quiz_ans_{q_index}_{option_index}
    _, _, q_index_str, opt_index_str = data.split("_")
    q_index = int(q_index_str)
    opt_index = int(opt_index_str)

    current_index = context.user_data.get("quiz_index", 0)
    if q_index != current_index:
        # Eskirgan tugma bosilgan, e'tiborsiz qoldiramiz
        return

    question = quiz.QUESTIONS[q_index]
    _, is_correct = question["options"][opt_index]
    if is_correct:
        context.user_data["quiz_score"] = context.user_data.get("quiz_score", 0) + 1
        await query.message.reply_text("✅ To'g'ri!")
    else:
        await query.message.reply_text("❌ Unchalik emas.")

    next_index = q_index + 1
    if next_index < len(quiz.QUESTIONS):
        context.user_data["quiz_index"] = next_index
        next_question = quiz.QUESTIONS[next_index]
        await query.message.reply_text(
            f"{next_index + 1}-savol: {next_question['question']}",
            reply_markup=build_question_keyboard(next_index),
        )
    else:
        score = context.user_data.get("quiz_score", 0)
        title = quiz.get_title(score)
        await query.message.reply_text(
            f"🏁 Test tugadi!\n\nNatijangiz: {score}/{len(quiz.QUESTIONS)}\n\n{title}"
        )
        context.user_data.pop("quiz_score", None)
        context.user_data.pop("quiz_index", None)


# ---------- Asosiy ishga tushirish ----------

def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi. .env faylini tekshiring.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", show_menu))
    application.add_handler(CommandHandler("pair", pair_command))
    application.add_handler(CommandHandler("anniversary", anniversary_command))
    application.add_handler(CallbackQueryHandler(age_gate_callback, pattern="^age_"))
    application.add_handler(CallbackQueryHandler(lovers_callback, pattern="^love_"))
    application.add_handler(CallbackQueryHandler(quiz_callback, pattern="^quiz_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, free_chat))

    logger.info("Sevishganlar boti ishga tushdi...")
    application.run_polling()


if __name__ == "__main__":
    main()
