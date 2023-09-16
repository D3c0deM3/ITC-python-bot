from aiogram.dispatcher.filters.state import State, StatesGroup


class Description(StatesGroup):
    video_id = State()
    video_description = State()
