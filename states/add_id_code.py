from aiogram.dispatcher.filters.state import State, StatesGroup


class IdCode(StatesGroup):
    id_get = State()