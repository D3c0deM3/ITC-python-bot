from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Mening hozirgi darajam📈"),
        ],
    ],
    resize_keyboard=True
)
