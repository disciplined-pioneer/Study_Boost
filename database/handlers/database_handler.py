import aiosqlite

# Регистрация пользователей с обновлением данных при совпадении по ID_user
async def register_user(user_data):
    database_path = 'database/data/users.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            # Используем `INSERT OR REPLACE` для автоматического обновления при совпадении
            await db.execute(''' 
                INSERT OR REPLACE INTO users 
                (ID_user, telegram, name_user, city_university, name_university, faculty, course, ID_message, photo_payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['ID_user'],
                user_data['telegram'],
                user_data['name_user'],
                user_data['city_university'],
                user_data['name_university'],
                user_data['faculty'],
                user_data['course'],
                user_data['ID_message'],
                user_data['photo_payment']
            ))
            await db.commit()
            return 'Данные успешно обновлены!'
        except Exception as e:
            print(f"Ошибка при регистрации пользователя: {e}")
            return 'Произошла ошибка при регистрации!'

# Добавление статуса подписки
async def add_subscription_status(ID_user, status):
    database_path = 'database/data/subscription_status.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            # Проверяем, существует ли пользователь в таблице подписок
            async with db.execute('SELECT * FROM subscription_status WHERE ID_user = ?', (ID_user,)) as cursor:
                existing_user = await cursor.fetchone()

            if existing_user:
                # Если пользователь существует, обновляем статус
                await db.execute('''
                    UPDATE subscription_status
                    SET status = ?
                    WHERE ID_user = ?
                ''', (status, ID_user))
                await db.commit()
                return 'Статус подписки успешно обновлен!'
            else:
                # Если пользователя нет, добавляем новую запись
                await db.execute(''' 
                    INSERT INTO subscription_status (ID_user, status)
                    VALUES (?, ?)
                ''', (ID_user, status))
                await db.commit()
                return 'Статус подписки успешно добавлен!'
        except Exception as e:
            print(f"Ошибка при добавлении/обновлении статуса подписки: {e}")
            return 'Произошла ошибка при добавлении/обновлении статуса подписки!'

# Добавление платежа
async def add_payment(ID_user, payment_date, expiration_date):
    database_path = 'database/data/payments.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            # Проверяем, существует ли пользователь в таблице платежей
            async with db.execute('SELECT * FROM payments WHERE ID_user = ?', (ID_user,)) as cursor:
                existing_payment = await cursor.fetchone()

            if existing_payment:
                # Если запись существует, обновляем её
                await db.execute('''
                    UPDATE payments
                    SET payment_date = ?, expiration_date = ?
                    WHERE ID_user = ?
                ''', (payment_date, expiration_date, ID_user))
                await db.commit()
                return 'Данные о платеже успешно обновлены!'
            else:
                # Если записи нет, добавляем новую
                await db.execute(''' 
                    INSERT INTO payments (ID_user, payment_date, expiration_date)
                    VALUES (?, ?, ?)
                ''', (ID_user, payment_date, expiration_date))
                await db.commit()
                return 'Платеж успешно добавлен!'
        except Exception as e:
            print(f"Ошибка при добавлении/обновлении платежа: {e}")
            return 'Произошла ошибка при добавлении/обновлении платежа!'
        

# Добавление рейтинга пользователя
async def add_or_update_user_rating(ID_user, rating):
    database_path = 'database/data/users_rating.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            # Используем `INSERT OR REPLACE` для автоматического обновления при совпадении
            await db.execute(''' 
                INSERT OR REPLACE INTO users_rating 
                (ID_user, rating)
                VALUES (?, ?)
            ''', (ID_user, rating))
            await db.commit()
            return 'Рейтинг пользователя успешно обновлён!'
        except Exception as e:
            print(f"Ошибка при добавлении/обновлении рейтинга пользователя: {e}")
            return 'Произошла ошибка при добавлении/обновлении рейтинга!'

# Добавление критерий оценки
async def add_rating_criteria(action_type, value_rating):
    database_path = 'database/data/rating_criteria.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            # Добавляем новый критерий
            await db.execute(''' 
                INSERT INTO rating_criteria (action_type, value_rating)
                VALUES (?, ?)
            ''', (action_type, value_rating))
            await db.commit()
            return 'Критерий рейтинга успешно добавлен!'
        except Exception as e:
            print(f"Ошибка при добавлении критерия рейтинга: {e}")
            return 'Произошла ошибка при добавлении критерия рейтинга!'
        
# Расчёт рейтинаг пользователя
async def add_rating_calculation(ID_user, rating_value, action_type):
    database_path = 'database/data/rating_calculation.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            await db.execute(''' 
                INSERT INTO rating_calculation (ID_user, rating_value, action_type)
                VALUES (?, ?, ?)
            ''', (ID_user, rating_value, action_type))
            await db.commit()
            return 'Расчёт рейтинга успешно добавлен!'
        except Exception as e:
            print(f"Ошибка при добавлении расчёта рейтинга: {e}")
            return 'Произошла ошибка при добавлении расчёта рейтинга!'


# Добавление советов   
async def add_user_advice(ID_user, date_publication, content, grade_advice):
    database_path = 'database/data/users_advice.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            await db.execute(''' 
                INSERT INTO users_advice (ID_user, date_publication, content, grade_advice)
                VALUES (?, ?, ?, ?)
            ''', (ID_user, date_publication, content, grade_advice))
            await db.commit()
            return 'Совет пользователя успешно добавлен!'
        except Exception as e:
            print(f"Ошибка при добавлении совета пользователя: {e}")
            return 'Произошла ошибка при добавлении совета пользователя!'

