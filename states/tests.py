from aiogram.dispatcher.filters.state import State, StatesGroup


class Test(StatesGroup):
    test_level = State()
    test_num = State()
    test_ids = State()


