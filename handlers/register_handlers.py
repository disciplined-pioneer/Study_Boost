from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.registration_keyb import registration_menu
from states.registration_states import RegistrationStates
from config import ADMIN_ID
from keyboards.admin_keyb import access_keyboard
from datetime import datetime

from database.requests.user_search import check_user_registration

# Хранение данных новых пользователей
new_users = []
router = Router()


# Обработчик для начала регистрации
@router.message(F.text == 'Регистрация 📝')
async def registration_handler(message: Message, state: FSMContext):

    # проверка на наличие пользователя в БД
    user_id = message.from_user.id
    result, _ = await check_user_registration(user_id)
    if result:
        await message.answer('УПС! Вы уже зарегистрированы! Пожалуйста, зайдите в систему с помощью пароля')
    else:
        await start_registration(message, state)

# Начало регистрации
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, укажите ваше имя: ")
    await state.set_state(RegistrationStates.name)  # Установить состояние ожидания имени

# Город университета
@router.message(F.text, RegistrationStates.name)
async def process_university_city(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохранить имя
    await message.answer("Введите город, в котором расположено ваше учебное заведение: ")
    await state.set_state(RegistrationStates.university_city)

# Название университета
@router.message(F.text, RegistrationStates.university_city)
async def process_name_university(message: Message, state: FSMContext):
    await state.update_data(university_city=message.text)  # Сохранить город университета
    await message.answer("Укажите полное название вашего учебного заведения: ")
    await state.set_state(RegistrationStates.name_university)

# Номер курса
@router.message(F.text, RegistrationStates.name_university)
async def process_course(message: Message, state: FSMContext):
    await state.update_data(name_university=message.text)  # Сохранить название университета
    await message.answer("На каком курсе вы обучаетесь? Пожалуйста, укажите номер курса: ")
    await state.set_state(RegistrationStates.course)

# Название курса
@router.message(F.text, RegistrationStates.course)
async def process_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)  # Сохранить номер курса
    await message.answer("Введите название вашего факультета: ")
    await state.set_state(RegistrationStates.faculty)  # Переход к следующему состоянию

# Название факультета
@router.message(F.text, RegistrationStates.faculty)
async def process_faculty(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)  # Сохранить название факультета
    await message.answer("Придумайте и введите пароль для вашей учётной записи: ")
    await state.set_state(RegistrationStates.password)  # Переход к следующему состоянию

# Ввод пароля для входа
@router.message(F.text, RegistrationStates.password)
async def process_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)  # Сохранить пароль
    await message.answer("Пожалуйста, отправьте фото, подтверждающее оплату:")
    await state.set_state(RegistrationStates.payment_photo)  # Переход к следующему состоянию

# Завершение регистрации и добавление пользователя в список
@router.message(F.photo, RegistrationStates.payment_photo)
async def finish_registration(message: Message, state: FSMContext):
    global new_users
    data = await state.get_data()
    user_id = message.from_user.id

    # Получаем фотографию оплаты
    payment_photo = message.photo[-1].file_id
    from datetime import datetime, timedelta
    # Сохраняем данные пользователя
    user_info = {
        "name_user": data.get("name"),
        "city_university": data.get("university_city"),
        "name_university": data.get("name_university"),
        "course": data.get("course"),
        "faculty": data.get("faculty"),
        "password": data.get('password'),
        "telegram": message.from_user.username,
        "ID_user": user_id,
        "ID_message": message.message_id,
        "photo_payment": payment_photo,
        "date_registration": datetime.now().date() - timedelta(days=100)

    }
    
    # Сохраняем user_id в состояние
    await state.update_data(user_id=user_id)  # Сохраняем user_id

    # Формируем текст для отправки админу
    user_info_text = (
        f"Имя: {data.get('name')}\n\n"
        f"Город университета: {data.get('university_city')}\n\n"
        f"Название университета: {data.get('name_university')}\n\n"
        f"Курс: {data.get('course')}\n\n"
        f"Факультет: {data.get('faculty')}\n\n"
        f"Телеграм: {message.from_user.username}\n\n"
        f"Пароль пользователя: {data.get('password')}\n\n"
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
    await message.answer('Поздравляем, регистрация успешно завершена! 🎉\n\n'
                    'В ближайшее время администратор проверит ваши данные и активирует подписку.\n\n'
                    'После этого вы получите уведомление. Желаем вам отличного дня!')

