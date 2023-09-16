import psycopg2
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import DB_HOST, DB_USER, DB_NAME, DB_PASS
from loader import dp
from states.grade_student import Grading


@dp.message_handler(text="Baho qo'yish")
async def handle_grade(message: types.Message):
    await Grading.id_code.set()
    await message.answer("Id kod kiriting")


@dp.message_handler(state=Grading.id_code)
async def handle_id_grade(message: types.Message, state: FSMContext):
    await state.update_data(id_code=message.text)
    await message.answer("Ball ni kiriting")
    await Grading.grade_num.set()


@dp.message_handler(state=Grading.grade_num)
async def handle_grade_num(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_code = data["id_code"]
    grade_score = int(message.text)

    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

    cursor = connection.cursor()

    cursor.execute("SELECT rating FROM users WHERE id_code = %s", (id_code,))
    row = cursor.fetchone()
    new_grade = int(row[0]) + grade_score

    # Execute the SQL update statement
    cursor.execute("UPDATE users SET rating = %s WHERE id_code = %s", (new_grade, id_code))

    # Commit the changes to the database
    connection.commit()

    # Close the database connection
    connection.close()

    await state.finish()
    await message.answer("Qo'shildi")
