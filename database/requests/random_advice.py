import random
import aiosqlite

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
        # Получаем советы по типу, включая ID пользователя
        cursor = await db.execute('SELECT content, ID_user FROM users_advice WHERE type_advice = ?', (advice_type,))
        all_advices = await cursor.fetchall()

        if all_advices:
            # Выбираем случайный совет
            random_advice = random.choice(all_advices)  # Получаем текст совета и ID пользователя
            return random_advice[0], random_advice[1]  # Возвращаем текст совета и ID пользователя
        else:
            return "К сожалению, нет доступных советов по этой категории", None  # Возвращаем None, если пользователь не найден
