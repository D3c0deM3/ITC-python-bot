from aiogram.dispatcher.filters.state import State, StatesGroup


class AdditionLesson(StatesGroup):
    what_id = State()
    level_num = State()
    lesson_num = State()
    wait_for_id = State()