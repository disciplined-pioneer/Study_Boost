import aiosqlite

async def create_db(DATABASE):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ID_user INTEGER UNIQUE,
                telegram TEXT UNIQUE,
                name_user TEXT,
                city_university TEXT,
                name_university TEXT,
                course TEXT,
                faculty TEXT,
                password TEXT,
                ID_message INTEGER,
                photo_payment TEXT
            )
        ''')
        await db.commit()
