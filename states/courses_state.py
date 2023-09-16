from aiogram.dispatcher.filters.state import State, StatesGroup


class GetLesson(StatesGroup):
    level = State()
    confirm_or_not = State()
    lesson = State()
