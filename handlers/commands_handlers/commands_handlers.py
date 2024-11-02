import aiosqlite
from datetime import datetime


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
            