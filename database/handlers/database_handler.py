import aiosqlite
from datetime import date, time

# Регистрация пользователей с обновлением данных при совпадении по ID_user
async def register_user(user_data):
    database_path = 'database/data/users.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            # Используем `INSERT OR REPLACE` для автоматического обновления при совпадении
            await db.execute(''' 
                INSERT OR REPLACE INTO users 
                (ID_user, telegram, referrer_id, name_user, city_university, name_university, faculty, course, ID_message, photo_payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['ID_user'],
                user_data['telegram'],
                user_data['referrer_id'],
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
        

# Добавление истории рейтинга пользователя
async def add_user_rating_history(advice_id:str, material_id:str, id_user: int, granted_by: int, accrual_date: str, action_type: str, rating_value: str):
    database_path = 'database/data/users_rating_history.db'
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute('''
            INSERT INTO users_rating_history (advice_id, material_id, id_user, granted_by, accrual_date, action_type, rating_value)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (advice_id, material_id, id_user, granted_by, accrual_date, action_type, rating_value))
        await db.commit()


# Добавление советов   
async def add_user_advice(ID_user, date_publication, content, type_advice, like_advice, dislike_advice):
    database_path = 'database/data/users_advice.db'
    async with aiosqlite.connect(database_path) as db:
        try:
            await db.execute(''' 
                INSERT INTO users_advice (ID_user, date_publication, content, type_advice, like_advice, dislike_advice)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (ID_user, date_publication, content, type_advice, like_advice, dislike_advice))
            await db.commit()
            return 'Совет пользователя успешно добавлен!'
        except Exception as e:
            print(f"Ошибка при добавлении совета пользователя: {e}")
            return 'Произошла ошибка при добавлении совета пользователя!'

# Добавление мероприятий
async def add_event(ID_user: int, date_publication: date, place: str, event_date: date, event_time: time, description: str):
    database_path = 'database/data/events.db'
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute('''
            INSERT INTO events (ID_user, date_publication, place, date, time, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (ID_user, date_publication, place, event_date, event_time, description))
        
        await db.commit()

# Добавление материалов
async def add_material(ID_user: int, date_publication: date, faculty: str, course: str, subject: str, type_material: str, 
                       topic: str, description_material: str, files_id: str, like_advice: str = "0", dislike_advice: str = "0"):
    database_path = 'database/data/materials.db'
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute('''
            INSERT INTO events (
                ID_user, 
                date_publication, 
                faculty, 
                course,
                subject,
                type_material,
                topic, 
                description_material, 
                files_id, 
                like_advice, 
                dislike_advice
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ID_user, date_publication, faculty, course, subject, type_material, 
              topic, description_material, files_id, like_advice, dislike_advice))
        
        await db.commit()


# Добавление помощи и предложений
async def add_help_suggestion(ID_user: int, suggestion_date: date, suggestion_type: str, content: str):
    database_path = 'database/data/help_suggestions.db'
    
    async with aiosqlite.connect(database_path) as db:
        await db.execute(''' 
            INSERT INTO events (ID_user, date, type, content)
            VALUES (?, ?, ?, ?)
        ''', (ID_user, suggestion_date, suggestion_type, content))
        
        await db.commit()