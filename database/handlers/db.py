import os
import aiosqlite
import asyncio

from database_create import create_db
from print_db import print_all_users
from database_handler import register_user

# Путь к базе данных
DB_DIR = 'database/data'
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DATABASE = os.path.join(DB_DIR, 'users.db')  # Полный путь к базе данных


async def main():
    await create_db(DATABASE)  # Создаем базу данных

    user_data = {
        'name_user': '1',
        'city_university': '1',
        'name_university': '1',
        'course': '1',
        'faculty': '1',
        'password': '1234567890',
        'telegram': 'yluxw',  # Исправлено на 'telegram'
        'ID_user': 802587774,
        'ID_message': 4023,
        'photo_payment': 'AgACAgIAAxkBAAIOAAFm_jJmOBbkizBpItkcc3ReDKshbAACIOIxG9U68Utm7tDbEIeFGQEAAwIAA3kAAzYE'
    }

    await register_user(user_data) # Регистрируем пользователя
    await print_all_users(DATABASE)  # Печатаем всех пользователей

if __name__ == '__main__':
    asyncio.run(main())
