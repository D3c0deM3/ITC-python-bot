from aiogram.dispatcher.filters.state import State, StatesGroup


class GetTest(StatesGroup):
    level = State()
    lesson = State()