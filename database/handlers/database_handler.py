import aiosqlite

# Регистрация пользователей
async def register_user(user_data, DATABASE):
    async with aiosqlite.connect(DATABASE) as db:
        try:
            await db.execute(''' 
                INSERT INTO users (ID_user, name_user, city_university, name_university, course, faculty, password, telegram, ID_message, photo_payment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_data['ID_user'],
                user_data['name_user'],
                user_data['city_university'],
                user_data['name_university'],
                user_data['course'],
                user_data['faculty'],
                user_data['password'],
                user_data['telegram'],
                user_data['ID_message'],
                user_data['photo_payment']
            ))
            await db.commit()
            print('Пользователь зарегистрирован!')  # Сообщение о успешной регистрации
        except aiosqlite.IntegrityError:
            print('Вы уже зарегистрированы!')  # Сообщение о повторной регистрации