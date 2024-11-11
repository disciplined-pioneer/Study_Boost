from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.help_suggestion_state import HelpSuggestionStates

router = Router()

@router.message(F.text == 'Оплата подписки 💵')
async def login_handler(message: Message):
    await message.answer('Здесь объясним как оплатить подписку и стоимость каждой из них')

@router.message(F.text == 'Инструкция 📕')
async def instruction_handler(message: Message):

    # Отправляем документ
    await message.bot.send_document(
        chat_id=message.from_user.id,
        document='BQACAgIAAxkBAAIQJWb-yNqpCOhKkViHeQp96c48vuHgAAKEaAAC1Tr5Sz35edJ2tLeBNgQ',
        caption = f'Инструкция содержит подробное описание всех функций платформы, пошаговое руководство по регистрации и использованию бота, а также примеры обмена учебными материалами и заработка очков за активность',
    )

@router.message(F.text == 'Создатель ©️')
async def creator_handler(message: Message):
    text = (
        "Привет, Я Virtu! 👨‍💻\n\n"
        "Я являюсь разработчиком этого Telegram-бота и Python-разработчиком, специализирующимся на Data Science 🤖\n\n"
        "Моя цель — создавать полезные и удобные инструменты, которые помогут студентам эффективно обмениваться знаниями и учебными материалами 📚\n\n"
        "Я студент первого курса, и этот бот был разработан для того, чтобы упростить жизнь студентов. Если у вас есть идеи или предложения, буду рад их услышать! 😉\n\n"
        "Для вопросов или предложений вы можете связаться со мной через почту virtu1129@gmail.com  📩"
    )

    # ID фотографии
    photo_id = 'AgACAgIAAxkBAAIIg2b6x72lvUPWCK_udjCgFdxTAAHamQAC2usxG3jT2UuwWltlE_cjTgEAAwIAA3kAAzYE'  # замените на фактический ID фотографии

    await message.answer_photo(photo=photo_id, caption=text, parse_mode='Markdown')

@router.message(F.text == 'Помощь ❓')
async def help_handler(message: Message, state: FSMContext):

    # Переходим в состояние "content", где пользователь будет вводить свой запрос
    await state.set_state(HelpSuggestionStates.content)
    await message.answer('Пожалуйста, опишите проблему, с которой вы столкнулись⚠️ \n\nНаш администратор свяжется с вами для уточнения и решения вашего вопроса!')

@router.message(HelpSuggestionStates.content)
async def help_content_handler(message: Message, state: FSMContext):
    user_question = message.text
    if user_question != '/cancellation':
        await state.update_data(question=user_question)

        await message.answer(f'Вы написали: {user_question}. Мы обработаем ваш запрос.')
        await state.clear()
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊')