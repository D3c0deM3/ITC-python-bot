from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


admin_confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ruxsat berish✅", callback_data="c_confirm"),
            InlineKeyboardButton(text="Rad etish⛔", callback_data="c_cancel"),

        ],
    ]
)