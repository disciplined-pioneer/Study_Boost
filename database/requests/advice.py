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

# Количество строчек в users_rating_history
async def check_rating_history(advice_id: int, granted_by: int) -> bool:
    database_path = 'database/data/users_rating_history.db'
    
    async with aiosqlite.connect(database_path) as db:
        # Выполняем запрос для подсчета строк, соответствующих условиям
        cursor = await db.execute('''
            SELECT COUNT(*) FROM users_rating_history
            WHERE advice_id = ? AND granted_by = ?
        ''', (advice_id, granted_by))
        
        count = await cursor.fetchone()  # Получаем результат
        total_count = count[0] if count else 0  # Получаем количество
        
        # Возвращаем True, если 0 или 1, иначе False
        return total_count <= 1
    
# Функция для получения последнего добавленного совета
async def get_last_advice_id() -> int:
    database_path = 'database/data/users_advice.db'
    
    async with aiosqlite.connect(database_path) as db:
        cursor = await db.execute('SELECT MAX(advice_id) FROM users_advice')
        advice_id = await cursor.fetchone()
        return advice_id[0] if advice_id else None