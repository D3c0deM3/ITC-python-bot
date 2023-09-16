from aiogram.dispatcher.filters.state import State, StatesGroup


class GetUser(StatesGroup):
    id_code = State()
    full_name = State()
    phone_number = State()
    tuman = State()
    school = State()
