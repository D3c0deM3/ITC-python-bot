from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


id_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="video"),
            KeyboardButton(text="document")
        ],
        [
            KeyboardButton(text="photo"),
            KeyboardButton(text="audio")
        ],
        [
            KeyboardButton(text="comments")
        ]
    ],
    resize_keyboard=True
)