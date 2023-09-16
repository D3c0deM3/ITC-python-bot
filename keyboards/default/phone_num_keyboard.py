from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

request_phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Raqamni jo'natish📲", request_contact=True),
        ]
    ],
    resize_keyboard=True
)