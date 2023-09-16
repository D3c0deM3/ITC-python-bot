from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

add_course = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Dars qo'shish➕"),
        ],
        [
            KeyboardButton(text="Id qo'shish"),
        ],
        [
            KeyboardButton(text="Qo'shimcha data yuklash"),
        ],
        [
            KeyboardButton(text="Baho qo'yish")
        ],
    ],
    resize_keyboard=True
)
