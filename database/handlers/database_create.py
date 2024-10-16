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

async def create_users_rating():
    database_path = 'database/data/users_rating.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users_rating (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER,
                rating TEXT
            )
        ''')
        await db.commit()

async def create_rating_criteria():
    database_path = 'database/data/rating_criteria.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS rating_criteria (
                rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT,
                value_rating TEXT
            )
        ''')
        
        # Вставка данных с правильными названиями колонок
        rating_data = [
            ('advice', '0.5'),
            ('material', '2'),
            ('like_advice', '1'),
            ('like_material', '1')
        ]

        await db.executemany('''
            INSERT INTO rating_criteria (action_type, value_rating) 
            VALUES (?, ?)
        ''', rating_data)

        await db.commit()

async def create_rating_calculation():
    database_path = 'database/data/rating_calculation.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS rating_calculation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER,
                rating_value TEXT,
                action_type TEXT
            )
        ''')
        await db.commit()


async def create_all_databases():
    await create_users_table()
    await create_subscription_status_table()
    await create_payments_table()
    await create_users_rating()
    await create_rating_criteria()
    await create_rating_calculation()