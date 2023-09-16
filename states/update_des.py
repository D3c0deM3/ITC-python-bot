from aiogram.dispatcher.filters.state import State, StatesGroup


class DesUpdate(StatesGroup):
    video_description_update = State()
