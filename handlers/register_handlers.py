from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.registration_keyb import registration_menu
from states.registration_states import RegistrationStates
from config import ADMIN_ID
from keyboards.admin_keyb import access_keyboard

# Хранение данных новых пользователей
new_users = []  # Глобальный список новых пользователей

router = Router()

# Приветственное сообщение
async def show_welcome(message: Message):
    await message.answer(
        'Добро пожаловать в @StudyBoost_bot! 🎓\n\n'
        'Этот бот создан для студентов, чтобы облегчить обмен знаниями и ресурсами. Здесь вы можете:\n\n'
        '🔹 Обмениваться конспектами и лабораторными работами: Делитесь своими материалами и получайте доступ к работам других студентов.\n\n'
        '🔹 Зарабатывать очки: Активное участие в платформе вознаграждается! Набирайте очки за взаимодействие, и первые три студента с наибольшим количеством очков получат денежные призы по итогам месяца.\n\n'
        '🔹 Узнавать о преподавателях: Ознакомьтесь с рейтингом преподавателей и их ожиданиями от студентов.\n\n'
        '🔹 Следить за расписанием: Используйте календарь для напоминаний о семинарах и дедлайнах.\n\n'
        '🔹 Организовывать мероприятия: Присоединяйтесь к тусовкам и мероприятиям, чтобы познакомиться с другими студентами и расширить кругозор.\n\n'
        '🔹 Получать советы: Читайте полезные советы, чтобы улучшить свою учебу и организовать время.\n\n'
        'Присоединяйтесь к нам и сделайте свою учебу проще и интереснее! 📚✨',
        reply_markup=registration_menu
    )

# Обработчик команды /start
@router.message(F.text == '/start')
async def start_handler(message: Message):
    await show_welcome(message)

# Обработчик для начала регистрации
@router.message(F.text == 'Регистрация 📝')
async def registration_handler(message: Message, state: FSMContext):
    await start_registration(message, state)

# Начало регистрации
async def start_registration(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(RegistrationStates.name)  # Установить состояние ожидания имени

# Город университета
@router.message(F.text, RegistrationStates.name)
async def process_university_city(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Сохранить имя
    await message.answer("Введите город, в котором расположен ваш университет: ")
    await state.set_state(RegistrationStates.university_city)

# Название университета
@router.message(F.text, RegistrationStates.university_city)
async def process_name_university(message: Message, state: FSMContext):
    await state.update_data(university_city=message.text)  # Сохранить город университета
    await message.answer("Введите название университета: ")
    await state.set_state(RegistrationStates.name_university)

# Номер курса
@router.message(F.text, RegistrationStates.name_university)
async def process_course(message: Message, state: FSMContext):
    await state.update_data(name_university=message.text)  # Сохранить название университета
    await message.answer("Введите номер вашего курса: ")
    await state.set_state(RegistrationStates.course)

# Название факультета
@router.message(F.text, RegistrationStates.course)
async def process_faculty(message: Message, state: FSMContext):
    await state.update_data(course=message.text)  # Сохранить номер курса
    await message.answer("Введите название вашего факультета: ")
    await state.set_state(RegistrationStates.faculty)

# Запрос фото оплаты
@router.message(F.text, RegistrationStates.faculty)
async def request_payment_photo(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)  # Сохранить факультет
    await message.answer("Пожалуйста, отправьте фото оплаты:")
    await state.set_state(RegistrationStates.payment_photo)

# Завершение регистрации и добавление пользователя в список
@router.message(F.photo, RegistrationStates.payment_photo)
async def finish_registration(message: Message, state: FSMContext):
    global new_users  # Объявляем new_users глобальной переменной
    data = await state.get_data()
    user_id = message.from_user.id

    # Получаем фотографию оплаты
    payment_photo = message.photo[-1].file_id

    # Сохраняем данные пользователя
    user_info = {
        "Имя": data.get("name"),
        "Город университета": data.get("university_city"),
        "Название университета": data.get("name_university"),
        "Курс": data.get("course"),
        "Факультет": data.get("faculty"),
        "ID пользователя": user_id,
        "Фото оплаты": payment_photo,
    }
    
    # Сохраняем user_id в состояние
    await state.update_data(user_id=user_id)  # Сохраняем user_id

    # Формируем текст для отправки админу
    user_info_text = (
        f"Имя: {data.get('name')}\n"
        f"Город университета: {data.get('university_city')}\n"
        f"Название университета: {data.get('name_university')}\n"
        f"Курс: {data.get('course')}\n"
        f"Факультет: {data.get('faculty')}\n"
        f"ID пользователя: {user_id}"
    )
    
    # Отправляем информацию админу
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=payment_photo,
        caption=user_info_text,
        reply_markup=access_keyboard
    )

    new_users.append(user_info)  # Добавляем пользователя в глобальный список
    await message.answer("Регистрация завершена! 🎉")
