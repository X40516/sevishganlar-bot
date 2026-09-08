"""
FSM (Finite State Machine) holatlari.
"""
from aiogram.fsm.state import State, StatesGroup


class LetterStates(StatesGroup):
    waiting_text = State()
    waiting_photo = State()
    confirm = State()


class QuestionStates(StatesGroup):
    answering = State()


class GameStates(StatesGroup):
    know_answering = State()


class MemoryStates(StatesGroup):
    waiting_photo = State()
    waiting_caption = State()


class DaysStates(StatesGroup):
    waiting_date = State()


class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_new_question = State()
    waiting_new_gift = State()
    waiting_ban_target = State()


class SupportStates(StatesGroup):
    chatting = State()
