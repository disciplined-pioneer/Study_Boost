import os
import aiosqlite

# Создание таблиц с информацией пользователях
async def create_users_table():
    database_path = 'database/data/users.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER UNIQUE,
                telegram TEXT UNIQUE,
                referrer_id TEXT,
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


# Таблица для хранения истории рейтинга пользователей
async def create_users_rating_history():
    database_path = 'database/data/users_rating_history.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users_rating_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                advice_id INTEGER,
                id_user INTEGER,
                granted_by INTEGER,
                accrual_date DATE,
                action_type TEXT,
                rating_value TEXT
            )
        ''')
        await db.commit()

# Советы пользователей
async def create_users_advice():
    database_path = 'database/data/users_advice.db'
    os.makedirs(os.path.dirname(database_path), exist_ok=True)

    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users_advice (
                advice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER,
                date_publication TEXT,
                content TEXT,
                type_advice TEXT,
                like_advice TEXT,
                dislike_advice TEXT
            )
        ''')
        await db.commit()


# Создание всех таблиц
async def create_all_databases():

    # Инф. про пользователей
    await create_users_table()
    await create_subscription_status_table()
    await create_payments_table()

    # Рейтинг
    await create_users_rating_history()

    # Советы
    await create_users_advice()