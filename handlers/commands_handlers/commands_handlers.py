import aiosqlite
from datetime import datetime

# вывод первых 10 пользователей в рейтинге
async def get_top_10_users():

    # Определяем текущий месяц и год
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Путь к базе данных
    database_path = 'database/data/users_rating_history.db'
    
    async with aiosqlite.connect(database_path) as db:
        # SQL-запрос для получения топ-10 пользователей за текущий месяц по сумме рейтингов
        query = '''
        SELECT id_user, SUM(CAST(rating_value AS REAL)) AS total_rating
        FROM users_rating_history
        WHERE strftime('%Y', accrual_date) = ? AND strftime('%m', accrual_date) = ?
        GROUP BY id_user
        ORDER BY total_rating DESC
        LIMIT 10
        '''
        
        # Выполняем запрос, передавая параметры для года и месяца
        async with db.execute(query, (str(current_year), f"{current_month:02}")) as cursor:
            top_users = await cursor.fetchall()
        
        # Выводим пользователей и их рейтинг
        return top_users

# Вывод рейтинга пользователя
async def user_rating(id_user):

    # Определяем текущий месяц и год
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Путь к базе данных
    database_path = 'database/data/users_rating_history.db'
    
    async with aiosqlite.connect(database_path) as db:
        # SQL-запрос для получения рейтинга пользователя за текущий месяц
        query = '''
        SELECT SUM(CAST(rating_value AS REAL)) AS total_rating
        FROM users_rating_history
        WHERE id_user = ? AND strftime('%Y', accrual_date) = ? AND strftime('%m', accrual_date) = ?
        '''
        
        # Выполняем запрос, передавая параметры для id пользователя, года и месяца
        async with db.execute(query, (id_user, str(current_year), f"{current_month:02}")) as cursor:
            result = await cursor.fetchone()
        
        # Возвращаем рейтинг пользователя или 0, если нет записей
        return result[0] if result[0] is not None else 0

