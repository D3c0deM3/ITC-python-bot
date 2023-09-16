import sqlite3

import psycopg2
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS, DB_HOST, DB_NAME, DB_USER, DB_PASS
from handlers.users.commands_for_db import create_table, insert_user_data, get_all_chat_ids, create_tests_table
from keyboards.default.add_lesson import add_course
from keyboards.default.courses_buttons import user_buttons
from keyboards.default.phone_num_keyboard import request_phone
from keyboards.inline.tests import section_levels, test_sections
from loader import dp, bot
from states.add_id_code import IdCode
from states.registration_state import GetUser
from states.tests import Test

codes = []


@dp.message_handler(text="Id qo'shish")
async def handle_add_id(message: types.Message):
    await message.answer("Maxsus ID-kodni kiriting")
    await IdCode.id_get.set()


@dp.message_handler(state=IdCode.id_get)
async def handle_id(message: types.Message, state: FSMContext):
    codes.append(message.text)
    await message.answer(f"ID-kod: {message.text} qo'shildi")
    await state.finish()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    create_table()
    try:
        all_chat_ids = get_all_chat_ids()
        if message.chat.id in all_chat_ids:
            await message.answer("Siz ro'yxatdan o'tgansiz. Botdan foydalanishingiz mumkin.", reply_markup=user_buttons)
            return
    except:
        print("User topilmadi")
    if str(message.chat.id) in str(ADMINS):
        await message.answer("Assalomu Aleykum, pastagi tugmalardan foydalanishingiz mumkin", reply_markup=add_course)
    else:
        await message.answer(
            f"Assalomu Aleykum, {message.from_user.full_name}. Botdan foydalanish uchun <b>ID-kod</b>ingizni kiriting!")
        await GetUser.id_code.set()


@dp.message_handler(state=GetUser.id_code)
async def handle_id_code(message: types.Message, state: FSMContext):
    if message.text in codes:
        await message.answer("Ism Sharifingizni yozing")
        await GetUser.full_name.set()
        await state.update_data(id_code=message.text)
    else:
        await message.answer("Ushbu ID-kod bizning ro'yxatda mavjud emas. Iltimos, aniqlashtirib qaytadan urunib "
                             "ko'ring.")
        return


@dp.message_handler(state=GetUser.full_name)
async def handle_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Telefon raqamingizni kiritish uchun quyidagi tugmani bosing", reply_markup=request_phone)
    await GetUser.phone_number.set()


@dp.message_handler(content_types=['contact'], state=GetUser.phone_number)
async def handle_contact(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer("Viloyat vva tumaningizni yozing")
    await GetUser.tuman.set()


@dp.message_handler(state=GetUser.tuman)
async def handle_tuman(message: types.Message, state: FSMContext):
    await state.update_data(tuman=message.text)
    await message.answer("Iltimos maktabingiz nomini yuboring\n"
                         "<b>Masalan:</b> 53-maktab")
    await GetUser.school.set()


@dp.message_handler(state=GetUser.school)
async def handle_school(message: types.Message, state: FSMContext):
    create_table()
    data = await state.get_data()
    insert_user_data(data["full_name"], data["phone_number"], data["id_code"], data["tuman"], message.text,
                     message.chat.id, 0)
    await message.answer("Tabriklaymiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz. O'qishlaringizga <b>OMAD</b>",
                         reply_markup=user_buttons)
    await state.finish()


@dp.message_handler(commands=['join_channel'])
async def join_channel(message: types.Message):
    # Replace 'YOUR_CHANNEL_INVITE_LINK' with the actual invite link of your channel
    channel_username = 'https://t.me/+FsZCN0Dchr05OGEy'

    try:
        # Get the information about the channel
        chat = await bot.get_chat(channel_username)

        # Check if the bot is already a member of the channel
        if chat.type == types.ChatType.CHANNEL and chat.get_member(bot.id) is None:
            # Add the bot as an administrator to the channel
            await bot.promote_chat_member(chat.id, bot.id, can_change_info=True, can_delete_messages=True,
                                          can_invite_users=True, can_restrict_members=True,
                                          can_pin_messages=True, can_promote_members=False)
            await message.reply('Bot added to the channel successfully!')
        else:
            await message.reply('Bot is already a member of the channel or the channel does not exist.')
    except Exception as e:
        await message.reply(f'Failed to add the bot to the channel: {str(e)}')


