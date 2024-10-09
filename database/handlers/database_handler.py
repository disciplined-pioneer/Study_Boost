import aiosqlite

# Регистрация пользователей
async def register_user(user_data):
    database_path = 'database/data/users.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            await db.execute(''' 
                INSERT INTO users (ID_user, telegram, name_user, city_university, name_university, course, faculty, ID_message, photo_payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['ID_user'],
                user_data['telegram'],
                user_data['name_user'],
                user_data['city_university'],
                user_data['name_university'],
                user_data['course'],
                user_data['faculty'],
                user_data['ID_message'],
                user_data['photo_payment']
            ))
            await db.commit()
        except aiosqlite.IntegrityError:
            return 'Вы уже зарегистрированы!'

# Добавление статуса подписки
async def add_subscription_status(ID_user, status):
    database_path = 'database/data/subscription_status.db'
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            INSERT INTO subscription_status (ID_user, status)
            VALUES (?, ?)
        ''', (ID_user, status))
        await db.commit()
        

# Добавление платежа
async def add_payment(ID_user, payment_date, expiration_date):
    database_path = 'database/data/payments.db'
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            INSERT INTO payments (ID_user, payment_date, expiration_date)
            VALUES (?, ?, ?)
        ''', (ID_user, payment_date, expiration_date))
        await db.commit()

