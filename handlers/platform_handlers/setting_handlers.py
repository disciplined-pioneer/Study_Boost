from datetime import datetime

from aiogram import types
from aiogram import Router, F
from aiogram.types import Message

from aiogram.fsm.context import FSMContext
from states.help_suggestion_state import HelpStates
from states.help_suggestion_state import SuggestionsStates

from keyboards.platform_keyb import platform_menu
from keyboards.cancellation_states import cancel_state

from NI_assistants.sentiment_text import analyze_sentiment
from database.requests.user_access import can_use_feature
from database.handlers.database_handler import add_help_suggestion

router = Router()

@router.message(F.text == 'Команды 📜')
async def commands_handler(message: Message):
    commands_text = (
        "<b>Доступные команды:</b>\n\n"
        "<b>/start</b> - Начало работы с ботом, активация и первоначальные настройки 🚀\n\n"
        "<b>/my_data</b> - Просмотр информации о вашем аккаунте, включая историю активности и личные данные 📊\n\n"
        "<b>/my_rating</b> - Отображение текущего рейтинга и прогресса ⭐\n\n"
        "<b>/referal_link</b> - Ваша уникальная реферальная ссылка для приглашения друзей 🔗\n\n"
        "<b>/my_referal</b> - Просмотр количества приглашённых вами друзей и описание ваших бонусов 👥\n\n"
        "<b>/top_users</b> - Список Топ-10 пользователей с наивысшим рейтингом 🏆\n\n"
        "<b>/subscription_status</b> - Информация о типе Вашей подписки 📅\n\n"
        "<b>/cancellation</b> - Отмена любого состояния ❌\n\n"
    )
    await message.reply(commands_text, parse_mode="HTML")

@router.message(F.text == 'Предложения ➕')
async def suggestions_handler(message: Message, state: FSMContext):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use > 0:

        # Переходим в состояние "content", где пользователь будет вводить свой запрос
        await state.set_state(SuggestionsStates.content)
        await message.reply('Пожалуйста, поделитесь вашим предложением или идеей💡 \n\nВаши мысли важны для нас, и мы обязательно рассмотрим их для улучшения нашего сервиса!', reply_markup=cancel_state)
    else:
        await message.reply(response_message)

@router.message(SuggestionsStates.content)
async def suggestions_content_handler(message: Message, state: FSMContext):

    user_id = message.from_user.id
    user_question = message.text

    if message.text not in ['/cancellation', 'Отменить ❌']:
        await state.update_data(question=user_question)

        # Проверка качества текста
        sentiment_score = await analyze_sentiment(message.text)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст", reply_markup=cancel_state)
            return
        else:
            await add_help_suggestion(ID_user=user_id,
                                    suggestion_date=datetime.now().date(),
                                    suggestion_type='suggestions',
                                    content=user_question)
            await message.reply(
                f'Спасибо за ваш вклад! Мы обязательно рассмотрим Ваше предложение для улучшения платформы! 🙂', reply_markup=platform_menu)
            await state.clear()
    else:
        await state.clear()
        await message.reply('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=platform_menu)

@router.message(F.text == 'Помощь ❓')
async def help_handler(message: Message, state: FSMContext):

    # Переходим в состояние "content", где пользователь будет вводить свой запрос
    await state.set_state(HelpStates.content)
    await message.reply('Пожалуйста, опишите проблему, с которой вы столкнулись⚠️ \n\nНаш администратор свяжется с вами для уточнения и решения вашего вопроса!',
                reply_markup=cancel_state)

@router.message(HelpStates.content)
async def help_content_handler(message: Message, state: FSMContext):

    user_id = message.from_user.id
    user_question = message.text

    if user_question not in ['/cancellation', 'Отменить ❌']:
        await state.update_data(question=user_question)
        await add_help_suggestion(ID_user=user_id,
                                 suggestion_date=datetime.now().date(),
                                 suggestion_type='help',
                                 content=user_question)
        await message.reply(f'Спасибо! Мы обязательно предоставим вам помощь в использовании платформы. Пожалуйста, ожидайте нашего ответа! 🙂', reply_markup=platform_menu)
        await state.clear()
    else:
        await state.clear()
        await message.reply('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=platform_menu)

@router.message(F.text == "Назад 🔙")
async def back_handler(message: types.Message):

    await message.reply(f'Вы вернулись в главное меню 😊', reply_markup=platform_menu)