from aiogram.dispatcher.filters.state import State, StatesGroup


class Grading(StatesGroup):
    id_code = State()
    grade_num = State()

