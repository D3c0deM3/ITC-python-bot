import re

import psycopg2
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import DB_HOST, DB_USER, DB_NAME, DB_PASS, ADMINS
from keyboards.inline.conf_cancel_lv import admin_confirmation
from keyboards.inline.course_vide_button import lesson_buttons
from keyboards.inline.sections import section_buttons
from keyboards.inline.tests import section_levels, test_sections
from loader import dp, bot
from states.courses_state import GetLesson
from states.tests_state import GetTest


def create_pg_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


def close_pg_connection(conn):
    conn.close()


@dp.message_handler(text="Darslar")
async def handle_course(message: types.Message):
    await message.answer("Bo'limlardan birini tanlang", reply_markup=section_buttons)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('lv_'))
async def handle_course_name(call: types.CallbackQuery, state: FSMContext):
    await GetLesson.level.set()
    course = call.data.split('_')[1]
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT levels, id_code FROM users WHERE chat_id = {call.message.chat.id}")
    user_levels = cursor.fetchone()
    if int(course) != 1 and user_levels[0] is not None:
        if int(course) in user_levels[0]:
            await state.update_data(level=course)
            await call.message.delete()
            await call.message.answer(f"Bo'lim: {course}\nQuyidagi darslardan birini tanlang",
                                      reply_markup=lesson_buttons)
            await GetLesson.lesson.set()
        else:
            await bot.send_message(chat_id=ADMINS[0],
                                   text=f"{user_levels[1]} ID kodli foydalanuchi {course}-levelning ga ruxsat so'rayapti.",
                                   reply_markup=admin_confirmation)
            await call.message.delete()
            await call.message.answer(
                "Siz keyingi level darslarini ko'rishingiz uchun admin sizga ruxsat berishi kerak\n"
                "Sizning so'rovingiz adminga yuborildi agar sizga admin rusat bersa siz keyingi levelga o'tasiz!")
            await state.finish()
    elif int(course) == 1:
        await state.update_data(level=course)
        await call.message.delete()
        await call.message.answer(f"Bo'lim: {course}\nQuyidagi darslardan birini tanlang", reply_markup=lesson_buttons)
        await GetLesson.lesson.set()
    else:
        await bot.send_message(chat_id=ADMINS[0],
                               text=f"{user_levels[1]} ID kodli foydalanuchi {course}-level ga ruxsat so'rayapti.",
                               reply_markup=admin_confirmation)
        await call.message.delete()
        await call.message.answer("Siz keyingi level darslarini ko'rishingiz uchun admin sizga ruxsat berishi kerak\n"
                                  "Sizning so'rovingiz adminga yuborildi agar sizga admin rusat bersa siz keyingi levelga o'tasiz!")
        await state.finish()
    conn.close()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('c_'))
async def handle_confirmation(call: types.CallbackQuery):
    message = call.message.text
    id_pattern = r"T-(\d+)"
    id_match = re.search(id_pattern, message)
    id_number = int()
    if id_match:
        id_number = int(id_match.group(1))

    # This pattern will match the 6-level part
    level_pattern = r"(\d+)-level"
    level_match = re.search(level_pattern, message)
    level_number = int()
    if level_match:
        level_number = int(level_match.group(1))

    id_code = f'T-{id_number}'
    confirm_type = call.data.split("_")[1]
    if confirm_type == "confirm":
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id FROM users WHERE id_code = '{id_code}'")
        chat_id = cursor.fetchone()[0]

        cursor.execute(f"SELECT levels FROM users WHERE id_code = '{id_code}'")
        levels = cursor.fetchone()[0]
        if levels is None:
            cursor.execute(f"UPDATE users SET levels = ARRAY[{level_number}] WHERE id_code = '{id_code}'")
            conn.commit()
            await call.message.answer("Siz ruxsat berdingiz✅")
            await call.message.delete()
            await bot.send_message(chat_id=chat_id, text=f"Sizga {level_number}-level darslarini ko'rish uchun ruxsat "
                                                         f"berildi")
        elif levels is not None:
            cursor.execute(
                f"UPDATE users SET levels = array_append(levels, {level_number}) WHERE id_code = '{id_code}'")
            conn.commit()
            await call.message.answer("Siz ruxsat berdingiz✅")
            await call.message.delete()
            await bot.send_message(chat_id=chat_id, text=f"Sizga {level_number}-level darslarini ko'rish uchun ruxsat "
                                                         f"berildi")
        conn.close()
    elif confirm_type == "cancel":
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT chat_id FROM users WHERE id_code = '{id_code}'")
        chat_id = cursor.fetchone()[0]
        await bot.send_message(chat_id=chat_id, text=f"Sizga {level_number}-levelga o'tishga ruxsat berilmadi!")
        await call.message.answer("Siz rad etdingiz⛔")
        await call.message.delete()
        conn.close()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ls_'), state=GetLesson.lesson)
async def handle_lesson_num(call: types.CallbackQuery, state: FSMContext):
    lesson = call.data.split('_')[1]
    data = await state.get_data()
    level = data.get("level")

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    # Execute the query
    query = """
    SELECT * FROM course_data
    WHERE (document_ids IS NOT NULL
    OR video_ids IS NOT NULL
    OR photo_ids IS NOT NULL
    OR audio_ids IS NOT NULL
    OR description IS NOT NULL
    OR comments IS NOT NULL)
    AND level_number = %s
    AND lesson_number = %s
    ORDER BY (video_ids->>'timestamp')::timestamp,
             (document_ids->>'timestamp')::timestamp,
             (photo_ids->>'timestamp')::timestamp,
             (audio_ids->>'timestamp')::timestamp;
    """
    cursor.execute(query, (level, lesson))

    # Process the retrieved rows
    # Process the retrieved rows
    rows = cursor.fetchall()
    for row in rows:
        flattened_data = []
        print(row)
        for row in rows:
            if row[2] is not None:
                for video_data in row[2]:
                    key_value_pairs = list(video_data.items())
                    timestamp = float(key_value_pairs[0][1])
                    video_id = key_value_pairs[1][0]
                    description = key_value_pairs[1][1]
                    flattened_data.append(
                        {"type": "video", "id": video_id, "timestamp": timestamp, "description": description})

            if row[1] is not None:
                for doc_data in row[1]:
                    if isinstance(doc_data, dict):
                        for file_id, timestamp in doc_data.items():
                            flattened_data.append({"type": "document", "id": file_id, "timestamp": float(timestamp)})
                    else:
                        flattened_data.append({"type": "photo", "id": doc_data, "timestamp": None})

            if row[3] is not None:
                for photo_data in row[3]:
                    if isinstance(photo_data, dict):
                        for file_id, timestamp in photo_data.items():
                            flattened_data.append({"type": "photo", "id": file_id, "timestamp": float(timestamp)})
                    else:
                        flattened_data.append({"type": "photo", "id": photo_data, "timestamp": None})
            if row[4] is not None:
                for audio_data in row[4]:
                    if isinstance(audio_data, dict):
                        for file_id, timestamp in audio_data.items():
                            flattened_data.append({"type": "audio", "id": file_id, "timestamp": float(timestamp)})
                    else:
                        flattened_data.append({"type": "comment", "id": audio_data, "timestamp": None})
            if row[5] is not None:
                for comment in row[5]:
                    if isinstance(comment, dict):
                        for text, timestamp in comment.items():
                            flattened_data.append({"type": "comment", "id": text, "timestamp": float(timestamp)})
                    else:
                        flattened_data.append({"type": "comment", "id": comment, "timestamp": None})

        # Sort flattened_data by timestamp
        sorted_data = sorted(flattened_data, key=lambda x: x["timestamp"] if x["timestamp"] is not None else 0)

        # Process and send the sorted_data
        for data in sorted_data:
            if data["type"] == "document":
                await bot.send_document(document=data["id"], chat_id=call.message.chat.id)
            elif data["type"] == "photo":
                await bot.send_photo(photo=data["id"], chat_id=call.message.chat.id)
            elif data["type"] == "audio":
                await bot.send_audio(audio=data["id"], chat_id=call.message.chat.id)
            elif data["type"] == "video":
                await bot.send_video(video=data["id"], caption=data["description"], chat_id=call.message.chat.id)
            elif data["type"] == "comment":
                await bot.send_message(text=data["id"], chat_id=call.message.chat.id)
        cursor.close()
        conn.close()

        await state.finish()


@dp.message_handler(text="Darslar", state=GetLesson.lesson)
async def handle_course(message: types.Message, state: FSMContext):
    await message.answer("Bo'limlardan birini tanlang", reply_markup=section_buttons)
    await state.finish()


@dp.message_handler(text="Test")
async def handle_course(message: types.Message):
    await message.answer("Bo'limlardan birini tanlang", reply_markup=section_levels)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ts_'))
async def handle_course_name(call: types.CallbackQuery, state: FSMContext):
    await GetLesson.level.set()
    course = call.data.split('_')[1]
    await state.update_data(level=course)
    await call.message.delete()
    await call.message.answer(f"Bo'lim: {course}\nQuyidagi testlardan birini tanlang", reply_markup=test_sections)
    await GetTest.lesson.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('test_'), state=GetTest.lesson)
async def handle_lesson_num(call: types.CallbackQuery, state: FSMContext):
    lesson = call.data.split('_')[1]
    data = await state.get_data()
    level = data.get("level")

    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    # Execute the query
    query = """
    SELECT * FROM test_data
    WHERE (test_document_ids IS NOT NULL
    OR test_video_ids IS NOT NULL
    OR test_photo_ids IS NOT NULL
    OR test_description IS NOT NULL)
    AND test_level_number = %s
    AND test_number = %s;
    """
    cursor.execute(query, (level, lesson))

    # Process the retrieved rows
    rows = cursor.fetchall()
    for row in rows:
        document_ids = row[1]
        video_ids = row[2]
        photo_ids = row[3]
        description = row[4]

        # Process the document_ids, video_ids, photo_ids as needed
        if document_ids is not None:
            for document_id in document_ids:
                await bot.send_document(document=document_id, chat_id=call.message.chat.id, caption=description)
        if video_ids is not None:
            for video_id in video_ids:
                await bot.send_video(video=video_id, chat_id=call.message.chat.id, caption=description, )
        if photo_ids is not None:
            for photo_id in photo_ids:
                await bot.send_photo(photo=photo_id, chat_id=call.message.chat.id, caption=description,
                                     protect_content=True)

    cursor.close()
    conn.close()

    await state.finish()


@dp.message_handler(text="Test", state=GetTest.lesson)
async def handle_course(message: types.Message):
    await message.answer("Bo'limlardan birini tanlang", reply_markup=section_levels)
