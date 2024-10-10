from aiogram import Router, F
from datetime import datetime
from keyboards.platform_keyb import platform_menu
from database.requests.user_search import check_user_registration, check_user_payment
from aiogram import types
from aiogram.fsm.context import FSMContext
from states.payment_states import PaymentStates

from config import ADMIN_ID
from handlers.register_handlers import new_users
from keyboards.admin_keyb import access_keyboard

router = Router()

async def send_user_information(message: types.Message, state: FSMContext, data, user_id, payment_photo):

    # Сохраняем данные пользователя
    user_info = {
        "name_user": data.get("name"),
        "city_university": data.get("city_university"),
        "name_university": data.get("name_university"),
        "course": data.get("course"),
        "faculty": data.get("faculty"),
        "telegram": f"@{message.from_user.username}" if message.from_user.username else "Не указан",
        "ID_user": user_id,
        "ID_message": message.message_id,
        "photo_payment": payment_photo,
        "date_registration": datetime.now().date()  # - timedelta(days=100)
    }

    # Сохраняем user_id в состояние
    await state.update_data(user_id=user_id)  # Сохраняем user_id

    # Формируем текст для отправки админу
    user_info_text = (
        f"Имя: {data.get('name')}\n\n"
        f"Город университета: {data.get('city_university')}\n\n"
        f"Название университета: {data.get('name_university')}\n\n"
        f"Курс: {data.get('course')}\n\n"
        f"Факультет: {data.get('faculty')}\n\n"
        f"Телеграм: {'@' + message.from_user.username if message.from_user.username else 'Не указан'}\n\n"
        f"ID сообщения: {message.message_id}\n\n"
        f"ID пользователя: {user_id}\n\n"
    )
        
    # Отправляем информацию админу
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=payment_photo,
        caption=user_info_text,
        reply_markup=access_keyboard
    )

    new_users.append(user_info)  # Добавляем пользователя в глобальный список
    await message.answer('Ваши данные были отправлены администратору. Ожидайте результата проверки 😊')

@router.message(F.photo, PaymentStates.payment_photo)  # Используем фильтр для проверки типа контента
async def receive_payment_photo(message: types.Message, state: FSMContext):
    # Получаем ID последней фотографии
    photo_id = message.photo[-1].file_id
    
    # Получаем данные, которые были сохранены в состоянии
    user_data = await state.get_data()
    user_info = user_data.get("user_info")
    user_id = user_data.get("user_id")
    
    # Отправляем информацию админу
    await send_user_information(message, state, user_info, user_id, photo_id)
    
    # Завершаем состояние
    await state.clear()

@router.message(F.text == 'Войти в систему 🚪')
async def login_handler(message: types.Message, state: FSMContext):
    # Проверка наличия пользователя в БД
    user_id = message.from_user.id
    result, user_info = await check_user_registration(user_id)
    
    if result:
        # Проверяем, действует ли ещё подписка
        user_payment = await check_user_payment(user_id)
        
        if user_payment:
            expiration_date = user_payment[3]  # Предполагается, что expiration_date находится на 4-й позиции
            now_date = datetime.now().date()
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()

            if expiration_date > now_date:
                await message.answer(f'Добро пожаловать! Доступ к платформе открыт 😊', reply_markup=platform_menu)
            else:
                await message.answer(f'Ваша подписка не оплачена! Пожалуйста, отправьте фото с вашей оплатой: ')
                
                # Сохраняем информацию о пользователе в состояние
                await state.update_data(user_info=user_info, user_id=user_id)
                
                # Устанавливаем состояние ожидания фотографии
                await state.set_state(PaymentStates.payment_photo)
        else:
            await message.answer('Не найдены данные о платеже. Пожалуйста, свяжитесь с поддержкой.')
    else:
        await message.answer('Вы не были зарегистрированы! Пожалуйста, зарегистрируйтесь и попробуйте снова, нажав на кнопку "Регистрация 📝"!')
