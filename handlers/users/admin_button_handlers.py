import datetime
import json

import psycopg2
from psycopg2 import sql

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from data.config import DB_HOST, DB_USER, DB_NAME, DB_PASS
from keyboards.default.add_lesson import add_course
from keyboards.default.type_data_keyboard import id_buttons
from keyboards.inline.course_vide_button import lesson_buttons
from keyboards.inline.sections import section_buttons
from keyboards.inline.tests import section_levels, test_sections
from loader import dp
from states.add_additional_lesson import AdditionLesson
from states.add_dars_state import AddLesson
from states.add_test import AddTest
from states.des_video import Description
from states.update_des import DesUpdate


@dp.message_handler(text="Dars qo'shish➕")
async def handle_add_lesson(message: types.Message):
    await AddLesson.level_num.set()

    await message.answer("Levelni tanlang", reply_markup=section_buttons)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('lv_'), state=AddLesson.level_num)
async def handle_level_for_adding(call: types.CallbackQuery, state: FSMContext):
    course = call.data.split('_')[1]
    await state.update_data(level_num=course)
    await call.message.delete()
    await AddLesson.lesson_num.set()
    await call.message.answer("Lesson ni tanlang", reply_markup=lesson_buttons)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ls_'), state=AddLesson.lesson_num)
async def handle_lesson_number_adding(call: types.CallbackQuery, state: FSMContext):
    lesson_number = call.data.split('_')[1]
    await state.update_data(lesson_num=lesson_number)
    await call.message.delete()
    await AddLesson.lesson_name.set()
    await call.message.answer("Darsni nomini kiriting")


@dp.message_handler(state=AddLesson.lesson_name)
async def handle_name_lesson(message: types.Message, state: FSMContext):
    await state.update_data(lesson_name=message.text)
    await AddLesson.lesson_doc_id.set()
    await message.answer("Dars uchun video, fayl, yoki rasm yuboring")


data_lessons = []

import json


@dp.message_handler(state=AddLesson.lesson_doc_id, content_types=ContentTypes.ANY)
async def handle_doc_id(message: types.Message, state: FSMContext):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    # cursor.execute("DROP TABLE IF EXISTS course_data")
    # conn.commit()
    # Create the table if it doesn't exist
    cursor.execute(sql.SQL("""
    CREATE TABLE IF NOT EXISTS course_data (
        id SERIAL PRIMARY KEY,
        document_ids JSONB,
        video_ids JSONB,
        photo_ids JSONB,
        audio_ids JSONB,
        comments JSONB,
        description TEXT,
        level_number INTEGER,
        lesson_number INTEGER
    )
    """))
    conn.commit()

    data = await state.get_data()
    lesson_doc_id = data.get("lesson_doc_id")
    lesson_name = data.get("lesson_name")
    level_num = data.get("level_num")
    lesson_num = data.get("lesson_num")
    something = str()

    # Check if a row with the specified level_number and lesson_number exists
    check_existence_query = sql.SQL("""
        SELECT * FROM course_data
        WHERE level_number = %s AND lesson_number = %s
    """)
    cursor.execute(check_existence_query, (level_num, lesson_num))
    existing_entry = cursor.fetchone()

    # Delete the row if it exists
    if existing_entry:
        delete_query = sql.SQL("""
            DELETE FROM course_data
            WHERE level_number = %s AND lesson_number = %s
        """)
        cursor.execute(delete_query, (level_num, lesson_num))
        conn.commit()

    if message.content_type == types.ContentType.VIDEO:
        await state.finish()
        await message.answer("Endi video uchun description yuboring")
        await Description.video_id.set()
        await state.update_data(video_id=message.video.file_id)
        await Description.video_description.set()
        data_lessons.append(level_num)
        data_lessons.append(lesson_name)
        data_lessons.append(lesson_num)
    elif message.content_type == types.ContentType.PHOTO:
        something = {f"{message.photo[0].file_id}": f"{datetime.datetime.now().timestamp()}"}
        something_json = json.dumps(something)  # Convert dictionary to JSON string
        insert_query = sql.SQL("""
            INSERT INTO course_data (photo_ids, description, level_number, lesson_number)
            VALUES (%s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (something_json, lesson_name, level_num, lesson_num))
        conn.commit()

        cursor.close()
        conn.close()

        await state.finish()
        await message.answer("Qo'shildi")
    elif message.content_type == types.ContentType.DOCUMENT:
        something = {f"{message.document.file_id}": f"{datetime.datetime.now().timestamp()}"}
        something_json = json.dumps(something)  # Convert dictionary to JSON string
        insert_query = sql.SQL("""
            INSERT INTO course_data (document_ids, description, level_number, lesson_number)
            VALUES (%s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (something_json, lesson_name, level_num, lesson_num))
        conn.commit()

        cursor.close()
        conn.close()
        await state.finish()
        await message.answer("Qo'shildi")
    elif message.text:
        something = {f"{message.text}": f"{datetime.datetime.now().timestamp()}"}
        something_json = json.dumps(something)  # Convert dictionary to JSON string
        insert_query = sql.SQL("""
                INSERT INTO course_data (comments, description, level_number, lesson_number)
                VALUES (%s, %s, %s, %s)
            """)
        cursor.execute(insert_query, (something_json, lesson_name, level_num, lesson_num))
        conn.commit()

        cursor.close()
        conn.close()

        await state.finish()
        await message.answer("Qo'shildi")
    elif message.content_type == types.ContentType.AUDIO:
        something = {f"{message.audio.file_id}": f"{datetime.datetime.now().timestamp()}"}
        something_json = json.dumps(something)  # Convert dictionary to JSON string
        insert_query = sql.SQL("""
            INSERT INTO course_data (audio_ids, description, level_number, lesson_number)
            VALUES (%s, %s, %s, %s)
        """)
        cursor.execute(insert_query, (something_json, lesson_name, level_num, lesson_num))
        conn.commit()

        cursor.close()
        conn.close()

        await state.finish()
        await message.answer("Qo'shildi")
    else:
        await message.answer("Unsupported content type. Please send a valid picture, video, or document.")
        return


@dp.message_handler(state=Description.video_description)
async def handle_description(message: types.Message, state: FSMContext):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    data = await state.get_data()
    video_id = data["video_id"]
    import json

    video_ids = [
        {f"{video_id}": f"{message.text}", "timestamp": f"{datetime.datetime.now().timestamp()}"},
    ]
    # Convert the video IDs object to JSON string
    video_ids_json = json.dumps(video_ids)
    insert_query = sql.SQL("""
        INSERT INTO course_data (video_ids, description, level_number, lesson_number)
        VALUES (%s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (video_ids_json, data_lessons[1], data_lessons[0], data_lessons[2]))
    conn.commit()
    data_lessons.clear()

    cursor.close()
    conn.close()

    await state.finish()
    await message.answer("Qo'shildi")


@dp.message_handler(text="Qo'shimcha data yuklash")
async def handle__add_more(message: types.Message):
    await AdditionLesson.level_num.set()
    await message.answer("Quyidagi levellar birini tanlang", reply_markup=section_buttons)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('lv_'), state=AdditionLesson.level_num)
async def handle_addition(call: types.CallbackQuery, state: FSMContext):
    course = call.data.split('_')[1]
    await state.update_data(level_number=course)
    await call.message.delete()
    await call.message.answer("Lesson ni tanlang", reply_markup=lesson_buttons)
    await AdditionLesson.lesson_num.set()


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ls_'),
                           state=AdditionLesson.lesson_num)
async def handle_lesson_add(call: types.CallbackQuery, state: FSMContext):
    lesson = call.data.split('_')[1]
    await state.update_data(lesson_number=lesson)
    await call.message.delete()
    await call.message.answer("Qaysi turdagi data yubormoqchisiz shuni bosing", reply_markup=id_buttons)
    await AdditionLesson.what_id.set()


@dp.message_handler(state=AdditionLesson.what_id)
async def handle_type_id(message: types.Message, state: FSMContext):
    await state.update_data(where_id=message.text)
    await AdditionLesson.wait_for_id.set()
    await message.answer(f"Endi {message.text} ni yuboring")


update_video = []


@dp.message_handler(state=AdditionLesson.wait_for_id, content_types=ContentTypes.ANY)
async def handle_wait_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    level = data["level_number"]
    where_id = data["where_id"]
    lesson = data["lesson_number"]
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    if message.content_type == types.ContentType.VIDEO:
        id_file = message.video.file_id
        update_video.append(id_file)
        await state.finish()
        await DesUpdate.video_description_update.set()
        await message.answer("Endi Description kiriting")
        update_video.append(level)
        update_video.append(lesson)
        update_video.append(where_id)
    elif message.content_type == types.ContentType.PHOTO:
        id_file = [{f"{message.photo[0].file_id}": f"{datetime.datetime.now().timestamp()}"}]
        something_json = json.dumps(id_file)
        cursor.execute(
            f"UPDATE course_data SET {where_id}_ids = COALESCE({where_id}_ids, '[]'::jsonb) || %s::jsonb WHERE level_number = %s AND lesson_number = %s",
            (something_json, level, lesson)
        )

        conn.commit()
        await message.answer("Qo'shildi", reply_markup=add_course)
        await state.finish()
    elif message.content_type == types.ContentType.DOCUMENT:
        id_file = [{f"{message.document.file_id}": f"{datetime.datetime.now().timestamp()}"}]
        something_json = json.dumps(id_file)
        cursor.execute(
            f"UPDATE course_data SET {where_id}_ids = COALESCE({where_id}_ids, '[]'::jsonb) || %s::jsonb WHERE level_number = %s AND lesson_number = %s",
            (something_json, level, lesson)
        )

        conn.commit()
        await message.answer("Qo'shildi", reply_markup=add_course)
        await state.finish()
    elif message.content_type == types.ContentType.AUDIO:
        id_file = [{f"{message.audio.file_id}": f"{datetime.datetime.now().timestamp()}"}]
        something_json = json.dumps(id_file)
        cursor.execute(
            f"UPDATE course_data SET {where_id}_ids = COALESCE({where_id}_ids, '[]'::jsonb) || %s::jsonb WHERE level_number = %s AND lesson_number = %s",
            (something_json, level, lesson)
        )

        conn.commit()
        update_video.clear()

        await message.answer("Qo'shildi", reply_markup=add_course)
        await state.finish()
    elif message.text:
        id_file = [{f"{message.text}": f"{datetime.datetime.now().timestamp()}"}]
        something_json = json.dumps(id_file)
        cursor.execute(
            f"UPDATE course_data SET comments = COALESCE(comments, '[]'::jsonb) || %s::jsonb WHERE level_number = %s AND lesson_number = %s",
            (something_json, level, lesson)
        )

        conn.commit()
        await message.answer("Qo'shildi", reply_markup=add_course)
        await state.finish()


@dp.message_handler(state=DesUpdate.video_description_update)
async def handle_desc_update(message: types.Message, state: FSMContext):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    print(update_video)
    id_file = update_video[0]
    level = update_video[1]
    lesson = update_video[2]

    # Prepare the video IDs JSONB object
    video_ids = [
        {f"{id_file}": f"{message.text}", "timestamp": f"{datetime.datetime.now().timestamp()}"}
    ]
    # Convert the video IDs object to JSON string
    video_ids_json = json.dumps(video_ids)
    cursor.execute(
        """
        UPDATE course_data
        SET video_ids = COALESCE(video_ids, '[]'::jsonb) || %s::jsonb
        WHERE level_number = %s AND lesson_number = %s
        """,
        (video_ids_json, level, lesson)
    )
    update_video.clear()
    conn.commit()
    await message.answer("Qo'shildi", reply_markup=add_course)
    await state.finish()


@dp.message_handler(text="Test qo'shish")
async def handle_add_lesson(message: types.Message):
    await AddTest.test_level.set()
    await message.answer("Test qo'shish uchun levelni tanlang", reply_markup=section_levels)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('ts_'), state=AddTest.test_level)
async def handle_level_for_adding(call: types.CallbackQuery, state: FSMContext):
    course = call.data.split('_')[1]
    await state.update_data(level_num=course)
    await call.message.delete()
    await AddTest.test_number.set()
    await call.message.answer("Test raqamini tanlang", reply_markup=test_sections)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('test_'), state=AddTest.test_number)
async def handle_lesson_number_adding(call: types.CallbackQuery, state: FSMContext):
    lesson_number = call.data.split('_')[1]
    await state.update_data(lesson_num=lesson_number)
    await call.message.delete()
    await AddTest.test_description.set()
    await call.message.answer("Test uchun description kiriting")


@dp.message_handler(state=AddTest.test_description)
async def handle_name_lesson(message: types.Message, state: FSMContext):
    await state.update_data(lesson_name=message.text)
    await AddTest.test_data_docs.set()
    await message.answer("Dars uchun video, fayl, yoki rasm yuboring")


@dp.message_handler(state=AddTest.test_data_docs, content_types=ContentTypes.ANY)
async def handle_doc_id(message: types.Message, state: FSMContext):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    # cursor.execute("DROP TABLE IF EXISTS course_data")
    # conn.commit()
    # Create the table if it doesn't exist
    cursor.execute(sql.SQL("""
    CREATE TABLE IF NOT EXISTS test_data (
        id SERIAL PRIMARY KEY,
        test_document_ids TEXT[],
        test_video_ids TEXT[],
        test_photo_ids TEXT[],
        test_description TEXT,
        test_level_number INTEGER,
        test_number INTEGER
    )
    """))
    conn.commit()

    data = await state.get_data()
    lesson_doc_id = data.get("lesson_doc_id")
    lesson_name = data.get("lesson_name")
    level_num = data.get("level_num")
    lesson_num = data.get("lesson_num")
    something = str()

    if message.content_type == types.ContentType.VIDEO:
        something = message.video.file_id
        insert_query = sql.SQL("""
            INSERT INTO test_data (test_video_ids, test_description, test_level_number, test_number)
            VALUES (%s, %s, %s, %s)
        """)
    elif message.content_type == types.ContentType.PHOTO:
        something = message.photo[0].file_id
        insert_query = sql.SQL("""
            INSERT INTO test_data (test_photo_ids, test_description, test_level_number, test_number)
            VALUES (%s, %s, %s, %s)
        """)
    elif message.content_type == types.ContentType.DOCUMENT:
        something = message.document.file_id
        insert_query = sql.SQL("""
            INSERT INTO test_data (test_document_ids, test_description, test_level_number, test_number)
            VALUES (%s, %s, %s, %s)
        """)
    else:
        await message.answer("Unsupported content type. Please send a valid picture, video, or document.")
        return

    cursor.execute(insert_query, ([something], lesson_name, level_num, lesson_num))
    conn.commit()

    cursor.close()
    conn.close()

    await state.finish()
    await message.answer("Qo'shildi")
