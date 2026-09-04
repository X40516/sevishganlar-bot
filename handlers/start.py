"""
/start buyrug'i, deep-link orqali juftlikka qo'shilish, asosiy menyu.
"""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.queries import (
    create_couple,
    get_couple_for_user,
    get_invite_by_code,
    get_partner_user,
    get_user_by_id,
    mark_invite_used,
)
from keyboards.reply import MENU_TEXTS, get_main_menu
from locales.texts import t

router = Router(name="start")


async def show_home(message: Message, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    couple = await get_couple_for_user(session, db_user.id)
    if couple is None:
        await message.answer(t(lang, "welcome"), reply_markup=get_main_menu(lang))
    else:
        await message.answer(t(lang, "home_menu"), reply_markup=get_main_menu(lang))


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    args = message.text.split(maxsplit=1)
    payload = args[1].strip() if len(args) > 1 else None

    if payload:
        couple = await get_couple_for_user(session, db_user.id)
        if couple is not None:
            await message.answer(t(lang, "already_paired"), reply_markup=get_main_menu(lang))
            return

        invite = await get_invite_by_code(session, payload)
        if invite is None:
            await message.answer(t(lang, "invite_invalid"))
            await show_home(message, session, db_user)
            return

        if invite.inviter_id == db_user.id:
            await message.answer(t(lang, "invite_self"))
            await show_home(message, session, db_user)
            return

        inviter = await get_user_by_id(session, invite.inviter_id)
        inviter_couple = await get_couple_for_user(session, invite.inviter_id) if inviter else None
        if inviter is None or inviter_couple is not None:
            await message.answer(t(lang, "invite_invalid"))
            await show_home(message, session, db_user)
            return

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=t(lang, "invite_accept"), callback_data=f"invite_accept:{invite.code}"),
                    InlineKeyboardButton(text=t(lang, "invite_reject"), callback_data=f"invite_reject:{invite.code}"),
                ]
            ]
        )
        await message.answer(t(lang, "invite_ask", name=inviter.full_name), reply_markup=kb)
        return

    await show_home(message, session, db_user)


@router.callback_query(F.data.startswith("invite_accept:"))
async def on_invite_accept(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    lang = db_user.language
    code = callback.data.split(":", 1)[1]
    invite = await get_invite_by_code(session, code)
    if invite is None:
        await callback.answer(t(lang, "invite_invalid"), show_alert=True)
        return

    existing_couple = await get_couple_for_user(session, db_user.id)
    inviter_couple = await get_couple_for_user(session, invite.inviter_id)
    if existing_couple is not None or inviter_couple is not None:
        await callback.answer(t(lang, "invite_invalid"), show_alert=True)
        return

    await create_couple(session, invite.inviter_id, db_user.id)
    await mark_invite_used(session, invite)

    await callback.message.edit_text(t(lang, "pair_success"))
    await callback.message.answer(t(lang, "home_menu"), reply_markup=get_main_menu(lang))

    inviter = await get_user_by_id(session, invite.inviter_id)
    if inviter:
        try:
            await callback.bot.send_message(
                inviter.telegram_id,
                t(inviter.language, "pair_success"),
                reply_markup=get_main_menu(inviter.language),
            )
        except Exception:
            pass
    await callback.answer()


@router.callback_query(F.data.startswith("invite_reject:"))
async def on_invite_reject(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await callback.message.edit_text(t(db_user.language, "invite_rejected"))
    await callback.answer()


@router.message(F.text.in_(MENU_TEXTS["menu_help"] | {"❓ Bot qanday ishlaydi?"}))
async def how_it_works(message: Message, db_user: User) -> None:
    await message.answer(t(db_user.language, "help_text"))


@router.callback_query(F.data == "menu:home")
async def go_home(callback: CallbackQuery, session: AsyncSession, db_user: User) -> None:
    await callback.message.answer(t(db_user.language, "home_menu"), reply_markup=get_main_menu(db_user.language))
    await callback.answer()
