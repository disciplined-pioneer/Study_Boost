import aiosqlite
import asyncio

async def check_user_registration(user_id, DATABASE):
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM users WHERE ID_user = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()  # Получаем только одну запись
            return bool(user)
