from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

section_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1-level", callback_data="lv_1"),
            InlineKeyboardButton(text="2-level", callback_data="lv_2")
        ],
        [
            InlineKeyboardButton(text="3-level", callback_data="lv_3"),
            InlineKeyboardButton(text="4-level", callback_data="lv_4")
        ],
        [
            InlineKeyboardButton(text="5-level", callback_data="lv_5"),
            InlineKeyboardButton(text="6-level", callback_data="lv_6")
        ],
        [
            InlineKeyboardButton(text="7-level", callback_data="lv_7"),
            InlineKeyboardButton(text="8-level", callback_data="lv_8")
        ],
        [
            InlineKeyboardButton(text="9-level", callback_data="lv_9"),
            InlineKeyboardButton(text="10-level", callback_data="lv_10")
        ],
        [
            InlineKeyboardButton(text="11-level", callback_data="lv_11"),
            InlineKeyboardButton(text="12-level", callback_data="lv_12")
        ],
    ]
)