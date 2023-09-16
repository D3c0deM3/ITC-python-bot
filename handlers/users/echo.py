from aiogram import types

from loader import dp


# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        await message.answer(message.text)
