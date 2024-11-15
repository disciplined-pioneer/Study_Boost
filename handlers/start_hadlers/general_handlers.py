from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.help_suggestion_state import HelpStates
from database.handlers.database_handler import add_help_suggestion

router = Router()

@router.message(F.text == 'Оплата подписки 💵')
async def login_handler(message: Message):
    await message.answer(
        "<b>🎉 Доступные подписки для @StudyBoost_bot</b>\n\n"
        "📅 <b>Basic Month:</b> подписка на 1 месяц — <b>50 ₽</b>\n\n"
        "📅 <b>Basic Two Month:</b> подписка на 2 месяца — <b>90 ₽</b> <i>(экономия 10%)</i> 🤑\n\n"
        "📅 <b>Three Month:</b> подписка на 3 месяца — <b>120 ₽</b> <i>(экономия 20%)</i> 🤑\n\n"
        "💎 <b>Premium:</b> <i>пожизненная стоимость в 25 ₽ для первых 50 пользователей</i> 🔥\n\n"
        "🔓 <b>Unlimited:</b> пожизненная подписка, которую можно получить, если по вашей реферальной ссылке перейдут и зарегистрируются <b>10 человек</b>!\n\n"
        "Для оформления подписки, пожалуйста, зарегистрируйтесь и переведите соответствующую сумму на:\n\n"
        "<b>Карта 🍀</b>: \"9104 0160 3996 20160\"\n"
        "<b>Переводила 📞</b>: \"+373-77-544-985 ( Максим Ш. )\"\n\n",
        parse_mode="HTML"
    )

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
    photo_id = 'AgACAgIAAxkBAAIIg2b6x72lvUPWCK_udjCgFdxTAAHamQAC2usxG3jT2UuwWltlE_cjTgEAAwIAA3kAAzYE'

    await message.answer_photo(photo=photo_id, caption=text, parse_mode='Markdown')

@router.message(F.text == 'Помощь ❓')
async def help_handler(message: Message, state: FSMContext):

    # Переходим в состояние "content", где пользователь будет вводить свой запрос
    await state.set_state(HelpStates.content)
    await message.answer('Пожалуйста, опишите проблему, с которой вы столкнулись⚠️ \n\nНаш администратор свяжется с вами для уточнения и решения вашего вопроса!')

@router.message(HelpStates.content)
async def help_content_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_question = message.text
    if user_question != '/cancellation':
        await state.update_data(question=user_question)
        await add_help_suggestion(ID_user=user_id,
                                    suggestion_date=datetime.now().date(),
                                    suggestion_type='help',
                                    content=user_question)
        await message.answer(
            f'Спасибо! Мы обязательно предоставим вам помощь в использовании платформы. Пожалуйста, ожидайте нашего ответа! 🙂'
        )
        await state.clear()
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊')