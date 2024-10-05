import aiosqlite

async def check_user_payment(user_id):
    DATABASE = "database/data/payments.db"
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute("SELECT * FROM payments WHERE ID_user = ?", (user_id,)) as cursor:
            user = await cursor.fetchone()  # Получаем только одну запись
            return user