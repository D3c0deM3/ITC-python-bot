from aiogram.dispatcher.filters.state import State, StatesGroup


class AddLesson(StatesGroup):
    level_num = State()
    lesson_num = State()
    lesson_name = State()
    lesson_doc_id = State()
    video_id = State()
