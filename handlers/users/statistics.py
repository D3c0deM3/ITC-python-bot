import psycopg2

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import DB_HOST, DB_USER, DB_NAME, DB_PASS
from loader import dp
import json

import telegraph
from aiogram import Bot, types, Dispatcher, executor

from states.courses_state import GetLesson

# Create an instance of the Telegraph class
telegraph_api = telegraph.Telegraph()

# Create the Telegraph account
telegraph_token = telegraph_api.create_account(short_name='ITCbot')


def retrieve_users_ordered_by_rating():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

    cursor = connection.cursor()

    # Retrieve all users ordered by their rating score
    cursor.execute("SELECT full_name, school, tuman, rating FROM users ORDER BY rating DESC")
    rows = cursor.fetchall()

    users = []
    for row in rows:
        user = {
            'full_name': row[0],
            'school': row[1],
            'tuman': row[2],
            'rating': row[3]
        }
        users.append(user)

    cursor.close()
    connection.close()

    return users


@dp.message_handler(text="Statistika")
async def handle_statistics(message: types.Message):
    # Get users by level order
    users = retrieve_users_ordered_by_rating()

    # Create the content of the page
    content = []
    content.append({'tag': 'h1', 'children': ['ITC statistics'], 'attrs': {'style': 'color: blue;'}})

    num = 0
    # Add the ratings to the content
    for user in users:
        num += 1
        user_text = f'{num}: {user["full_name"]}, Tuman: {user["tuman"]}, Maktab: {user["school"]}, ball: {user["rating"]}'
        content.append({'tag': 'p', 'children': [user_text], 'attrs': {'style': 'font-weight: bold;'}})

    # Create a new Telegraph page
    response = telegraph_api.create_page(
        title='Ratings',
        content=content,
        author_name='ITC'
    )

    # Get the URL of the published page
    ratings_message_url = response['url']

    # Send the Telegraph URL to the user
    await message.reply(f"Reyting natijalarini ko'rishingiz mumkin: {ratings_message_url}")



