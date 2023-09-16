
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

section_levels = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1-level", callback_data="ts_1"),
            InlineKeyboardButton(text="2-level", callback_data="ts_2")
        ],
        [
            InlineKeyboardButton(text="3-level", callback_data="ts_3"),
            InlineKeyboardButton(text="4-level", callback_data="ts_4")
        ],
        [
            InlineKeyboardButton(text="5-level", callback_data="ts_5"),
            InlineKeyboardButton(text="6-level", callback_data="ts_6")
        ],
        [
            InlineKeyboardButton(text="7-level", callback_data="ts_7"),
            InlineKeyboardButton(text="8-level", callback_data="ts_8")
        ],
        [
            InlineKeyboardButton(text="9-level", callback_data="ts_9"),
            InlineKeyboardButton(text="10-level", callback_data="ts_10")
        ],
        [
            InlineKeyboardButton(text="11-level", callback_data="ts_11"),
            InlineKeyboardButton(text="12-level", callback_data="ts_12")
        ],
    ]
)


test_sections = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1-test", callback_data="test_1"),
        ],
        [
            InlineKeyboardButton(text="2-test", callback_data="test_2"),
        ],
        [
            InlineKeyboardButton(text="3-test", callback_data="test_3"),
        ],
        [
            InlineKeyboardButton(text="4-test", callback_data="test_4"),
        ],
    ]
)
