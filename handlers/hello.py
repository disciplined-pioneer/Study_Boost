from aiogram import Router, F
from aiogram.types import Message
from keyboards.registration_keyb import registration_menu

from aiogram import types
from keyboards.registration_keyb import agreement


router = Router()

# Приветственное сообщение
async def show_welcome(message: Message):
    await message.answer(
        'Добро пожаловать в @StudyBoost_bot! 🎓\n\n'
        'Этот бот создан для студентов, чтобы облегчить обмен знаниями и ресурсами. Здесь вы можете:\n\n'
        '🔹 Обмениваться конспектами и лабораторными работами: Делитесь своими материалами и получайте доступ к работам других студентов.\n\n'
        '🔹 Зарабатывать очки: Активное участие в платформе вознаграждается! Набирайте очки за взаимодействие, и первые три студента с наибольшим количеством очков получат денежные призы по итогам месяца.\n\n'
        '🔹 Узнавать о преподавателях: Ознакомьтесь с рейтингом преподавателей и их ожиданиями от студентов.\n\n'
        '🔹 Организовывать мероприятия: Присоединяйтесь к тусовкам и мероприятиям, чтобы познакомиться с другими студентами и расширить кругозор.\n\n'
        '🔹 Получать советы: Читайте полезные советы, чтобы улучшить свою учебу и организовать время.\n\n'
        'Присоединяйтесь к нам и сделайте свою учебу проще и интереснее! 📚✨',
        reply_markup=registration_menu
    )

# Обработчик команды /start
@router.message(F.text == '/start')
async def start_handler(message: Message):

    # Отправляем документ
    await message.bot.send_document(
        chat_id=message.from_user.id,
        document='BQACAgIAAxkBAAIQJWb-yNqpCOhKkViHeQp96c48vuHgAAKEaAAC1Tr5Sz35edJ2tLeBNgQ',
        caption = f'Уважаемый пользователь, пожалуйста, ознакомьтесь с пользовательским соглашением!\n\nПосле прочтения нажмите на кнопку ниже с надписью "Я согласен ✅"',
        reply_markup=agreement
    )
    
@router.callback_query(F.data == "agreement_users")
async def handle_button_click(callback_query: types.CallbackQuery):
    await callback_query.answer("Благодарим за использование нашей платформы!")
    await show_welcome(callback_query.message)