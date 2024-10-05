import aiosqlite

async def check_user_registration(user_id):
    DATABASE = "database/data/users.db"
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users WHERE ID_user = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()  # Получаем только одну запись
            return bool(user), user
