import random
import aiosqlite

# Поиск пользователя по его ID
async def get_user_name(ID_user: int):
    database_path = 'database/data/users.db'
    
    async with aiosqlite.connect(database_path) as db:
        cursor = await db.execute('SELECT telegram FROM users WHERE ID_user = ?', (ID_user,))
        result = await cursor.fetchone()
        
        if result:
            return result[0]  # Возвращаем имя пользователя
        else:
            return None  # Если пользователь не найден

async def get_random_advice(advice_type: str):
    database_path = 'database/data/users_advice.db'
    async with aiosqlite.connect(database_path) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute('SELECT * FROM users_advice WHERE type_advice = ?', (advice_type,))
        all_advices = await cursor.fetchall()

        if all_advices:
            random_advice = random.choice(all_advices)
            return dict(random_advice)
        else:
            return None

