import aiosqlite
from datetime import datetime

# Вывод первых 10 пользователей в рейтинге
async def get_top_10_users():

    # Определяем текущий месяц и год
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Путь к базе данных
    database_path = 'database/data/users_rating_history.db'
    
    async with aiosqlite.connect(database_path) as db:
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

# Вывод информации о пользователе
async def fetch_user_data(user_id):
    database_path = 'database/data/users.db'
    
    async with aiosqlite.connect(database_path) as db:
        async with db.execute('''
            SELECT id, ID_user, telegram, referrer_id, name_user, city_university, name_university, faculty, course
            FROM users
            WHERE ID_user = ?
        ''', (user_id,)) as cursor:
            user_data = await cursor.fetchone()
            if user_data:
                return {
                    "id": user_data[0],
                    "ID_user": user_data[1],
                    "telegram": user_data[2],
                    "referrer_id": user_data[3],
                    "name_user": user_data[4],
                    "city_university": user_data[5],
                    "name_university": user_data[6],
                    "faculty": user_data[7],
                    "course": user_data[8],
                }
            else:
                return None  # Пользователь не найден

# Проверяем наличие подписки в таблице subscription_status
async def user_subscription(user_id):
    async with aiosqlite.connect('database/data/subscription_status.db') as db:
        async with db.execute('SELECT status FROM subscription_status WHERE ID_user = ?', (user_id,)) as cursor:
            subscription_data = await cursor.fetchone()
            return subscription_data

# Проверяем наличие информации об оплате в таблице payments
async def payment_information(user_id):
    async with aiosqlite.connect('database/data/payments.db') as db:
        async with db.execute('SELECT payment_date, expiration_date FROM payments WHERE ID_user = ?', (user_id,)) as cursor:
            payment_data = await cursor.fetchone()
            return payment_data
