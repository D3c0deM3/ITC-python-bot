from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTest(StatesGroup):
    test_level = State()
    test_number = State()
    test_description = State()
    test_data_docs = State()
