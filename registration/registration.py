from aiogram import Dispatcher, F
from aiogram.types import Message
from handlers.registration_hand import registration_menu  # Импортируем меню

async def show_welcome(message: Message):
    await message.answer(
        'Добро пожаловать в @StudyUp_bot! 🎓\n\n'
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


async def register_user(message: Message):
    # Логика регистрации пользователя
    await message.answer('Вы успешно зарегистрированы!')

def register_handlers(dp: Dispatcher):

    @dp.message(F.text == '/start')
    async def start_handler(message: Message):
        await show_welcome(message)  # Показываем приветственное сообщение с кнопками

    @dp.message(F.text == 'Регистрация 📝')
    async def registration_handler(message: Message):
        await register_user(message)

    @dp.message(F.text == 'Войти в систему 🚪')
    async def login_handler(message: Message):
        await message.answer('Запрашиваем данные на вход')

    @dp.message(F.text == 'Инструкция 📕')
    async def instruction_handler(message: Message):
        await message.answer('Здесь нужно отправить файл pdf')

    @dp.message(F.text == 'Создатель ©️')
    async def creator_handler(message: Message):
        await message.answer('Здесь отправляем мою фотографию и краткую информацию обо мне')

    @dp.message(F.text == 'Помощь ❓')
    async def help_handler(message: Message):
        await message.answer('Просим отправить вопрос, по которому пользователь хотел обратиться')