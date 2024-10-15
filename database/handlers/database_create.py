import os
import aiosqlite

# Создание таблицы пользователей
async def create_users_table():
    database_path = 'database/data/users.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER UNIQUE,
                telegram TEXT UNIQUE,
                name_user TEXT,
                city_university TEXT,
                name_university TEXT,
                faculty TEXT,
                course TEXT,
                ID_message INTEGER,
                photo_payment TEXT
            )
        ''')
        await db.commit()

async def create_subscription_status_table():
    database_path = 'database/data/subscription_status.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS subscription_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER,
                status TEXT,
                UNIQUE(ID_user)
            )
        ''')
        await db.commit()

async def create_payments_table():
    database_path = 'database/data/payments.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER,
                payment_date DATE,
                expiration_date DATE,
                UNIQUE(ID_user)
            )
        ''')
        await db.commit()

async def create_all_databases():
    await create_users_table()
    await create_subscription_status_table()
    await create_payments_table()