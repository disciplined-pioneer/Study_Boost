from aiogram import types
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.registration_keyb import registration_menu, agreement

router = Router()

# Приветственное сообщение
async def show_welcome(message: Message):
    await message.answer(
        'Добро пожаловать в @StudyBoost_bot! 🎓\n\n'
        'Этот бот создан для студентов, чтобы облегчить обмен знаниями и ресурсами. Здесь вы можете:\n\n'
        '🔹 Обмениваться конспектами и лабораторными работами: Делитесь своими материалами и получайте доступ к работам других студентов.\n\n'
        '🔹 Зарабатывать очки: Активное участие в платформе вознаграждается! Набирайте очки за взаимодействие, и первые три студента с наибольшим количеством очков получат денежные призы по итогам месяца.\n\n'
        '🔹 Организовывать мероприятия: Присоединяйтесь к тусовкам и мероприятиям, чтобы познакомиться с другими студентами и расширить кругозор.\n\n'
        '🔹 Получать советы: Читайте полезные советы, чтобы улучшить свою учебу и организовать время.\n\n'
        'Присоединяйтесь к нам и сделайте свою учебу проще и интереснее! 📚✨',
        reply_markup=registration_menu
    )

# Обработчик команды /start с реферальным кодом
@router.message(F.text.startswith('/start'))
async def start_handler(message: Message, state: FSMContext):

    # Проверяем, содержит ли команда аргумент (реферальный ID)
    args = message.text.split()
    referrer_id = args[1] if len(args) > 1 else 'None'
    #referrer_id = args[1] if len(args) > 1 and args[1] != str(message.from_user.id) else 'None'
    await state.update_data(referrer_id=referrer_id)
    welcome_message = f"Добро пожаловать!{' Вы пришли по реферальной ссылке от пользователя с ID: ' + referrer_id if referrer_id != 'None' else ''}"
    await message.answer(welcome_message)


    # Отправляем документ с соглашением
    await message.bot.send_document(
        chat_id=message.from_user.id,
        document='BQACAgIAAxkBAAIQJWb-yNqpCOhKkViHeQp96c48vuHgAAKEaAAC1Tr5Sz35edJ2tLeBNgQ',
        caption = 'Уважаемый пользователь, пожалуйста, ознакомьтесь с пользовательским соглашением!\n\n'
                  'После прочтения нажмите на кнопку ниже с надписью "Я согласен ✅"',
        reply_markup=agreement
    )

# Обработчик нажатия на кнопку соглашения
@router.callback_query(F.data == "agreement_users")
async def handle_button_click(callback_query: types.CallbackQuery):
    await callback_query.answer("Благодарим за использование нашей платформы!")
    await show_welcome(callback_query.message)