from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from keyboards.admin_keyb import access_keyboard
from states.registration_state import RegistrationStates

from database.requests.user_search import check_user_registration, count_users

# Хранение данных новых пользователей
new_users = []
router = Router()

# Обработчик для начала регистрации
@router.message(F.text == 'Регистрация 📝')
async def registration_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    result, _ = await check_user_registration(user_id)
    if result:
        await message.answer('УПС! Вы уже зарегистрированы! Пожалуйста, войдите в платформу, нажав на кнопку "Войти в систему 🚪"')
    else:
        await start_registration(message, state)

# Имя пользователя
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, укажите ваше имя: ")
    await state.set_state(RegistrationStates.name)

# Город университета
@router.message(F.text, RegistrationStates.name)
async def process_city_university(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите город, в котором расположено ваше учебное заведение: ")
    await state.set_state(RegistrationStates.city_university)

# Название университета
@router.message(F.text, RegistrationStates.city_university)
async def process_name_university(message: Message, state: FSMContext):
    await state.update_data(city_university=message.text)
    await message.answer("Укажите полное название вашего учебного заведения: ")
    await state.set_state(RegistrationStates.name_university)

# Название факультета
@router.message(F.text, RegistrationStates.name_university)
async def process_faculty(message: Message, state: FSMContext):
    await state.update_data(name_university=message.text)
    await message.answer("Введите название вашего факультета: ")
    await state.set_state(RegistrationStates.faculty)

# Номер курса
@router.message(F.text, RegistrationStates.faculty)
async def process_course(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)
    await message.answer("На каком курсе вы обучаетесь? Пожалуйста, укажите номер курса: ")
    await state.set_state(RegistrationStates.course)

# Фото оплаты
@router.message(F.text, RegistrationStates.course)
async def process_payment_photo(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await message.answer("Пожалуйста, отправьте фото, подтверждающее оплату: ")
    await state.set_state(RegistrationStates.payment_photo)

# Завершение регистрации и добавление пользователя в список
@router.message(F.photo, RegistrationStates.payment_photo)
async def finish_registration(message: Message, state: FSMContext):
    global new_users
    data = await state.get_data()
    user_id = message.from_user.id
    referrer_id = data.get("referrer_id")

    # Получаем фотографию оплаты
    payment_photo = message.photo[-1].file_id

    # Сохраняем данные пользователя
    user_info = {
        "name_user": data.get("name"),
        "city_university": data.get("city_university"),
        "name_university": data.get("name_university"),
        "faculty": data.get("faculty"),
        "course": data.get("course"),
        "telegram": f"@{message.from_user.username}" if message.from_user.username else "Не указан",
        "ID_user": user_id,
        "ID_message": message.message_id,
        "photo_payment": payment_photo,
        "referrer_id": referrer_id,
        "date_registration": datetime.now().date() #- timedelta(days=100)
    }

    # Формируем текст для отправки админу
    user_info_text = (
        f"Имя: {data.get('name')}\n\n"
        f"Город университета: {data.get('city_university')}\n\n"
        f"Название университета: {data.get('name_university')}\n\n"
        f"Факультет: {data.get('faculty')}\n\n"
        f"Курс: {data.get('course')}\n\n"
        f"Телеграм: {'@' + message.from_user.username if message.from_user.username else 'Не указан'}\n\n"
        f"ID сообщения: {message.message_id}\n\n"
        f"ID пользователя: {user_id}\n\n"
        f"ID реферера: {referrer_id or 'Отсутствует'}\n\n"
        f"Количество пользователей: {await count_users()}\n\n"
    )

    # Отправляем информацию админу
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=payment_photo,
        caption=user_info_text,
        reply_markup=access_keyboard
    )

    # Отправляем сообщение пользователю
    new_users.append(user_info)
    await message.answer(
        'Поздравляем, регистрация успешно завершена! 🎉\n\n'
        'В ближайшее время администратор проверит ваши данные и активирует подписку.\n\n'
        'После этого вы получите уведомление. Желаем вам отличного дня!'
    )
    await state.clear()