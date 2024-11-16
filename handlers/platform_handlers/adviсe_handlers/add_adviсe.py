from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.adviсe_state import AdviсeStates
from keyboards.cancellation_states import cancel_state
from keyboards.advice_keyb import category_keyboard, advice_menu

from database.requests.advice import get_last_advice_id
from database.requests.user_access import can_use_feature
from NI_assistants.sentiment_text import analyze_sentiment
from database.handlers.database_handler import add_user_advice, add_user_rating_history

router = Router()

@router.message(F.text == 'Добавить совет ➕')
async def start_add(message: Message, state: FSMContext):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply("Пожалуйста, выберите категорию:", reply_markup=category_keyboard)
    else:
        await message.answer(response_message)

# Обработчик нажатия на кнопки инлайн-клавиатуры для добавления совета
@router.callback_query(lambda c: c.data in ['study', 'health', 'social', 'work'])
async def category_selected(callback: CallbackQuery, state: FSMContext):

    if callback.data not in ['/cancellation', 'Отменить состояние']:

        user_id = callback.from_user.id
        can_use, response_message = await can_use_feature(user_id)

        if can_use:

            # Сохранение выбранной категории в состояние
            selected_category = callback.data
            await state.update_data(category_advice=selected_category)

            # Ответ пользователю и завершение обработки
            await callback.message.reply("Пожалуйста, введите текст вашего совета:", reply_markup=cancel_state)
            await callback.answer()
            await state.set_state(AdviсeStates.category_advice)

        else:
            await callback.answer(response_message)
    else:
        await state.clear()
        await callback.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=advice_menu)

# Обработчик для текста совета
@router.message(F.text, AdviсeStates.category_advice)
async def process_advice(message: Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить состояние']:
    
        data = await state.get_data()  # Получаем данные состояния
        user_id = message.from_user.id

        # Добавляем оставшиеся данные
        await state.update_data(date_publication=datetime.now().date())
        await state.update_data(ID_user=user_id)
        await state.update_data(content=message.text)

        # Проверка качества текста
        sentiment_score = await analyze_sentiment(message.text)
        if sentiment_score <= -0.01:
            await message.answer("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой совет", reply_markup=advice_menu)
            await state.clear()  # Завершаем состояние
            return

        # Сохраняем данные в БД и получаем ID добавленного совета
        data = await state.get_data()
        user_advice_response = await add_user_advice(
            ID_user=data.get('ID_user'),
            date_publication=data.get('date_publication'),
            content=data.get('content'),
            type_advice=data.get('category_advice'),
            like_advice='0',
            dislike_advice='0'
        )

        if user_advice_response == "Совет пользователя успешно добавлен!":
            
            # Получаем advice_id последнего добавленного совета
            advice_id = await get_last_advice_id()

            date = datetime.now().date()
            await add_user_rating_history(
                advice_id=advice_id,
                material_id='None',
                id_user=user_id,
                granted_by=user_id,
                accrual_date=date,
                action_type="add_advice",
                rating_value='0.5'
            )
            await message.answer(f"Спасибо за ваш вклад! Ваш совет был добавлен, и вы получили +0.5 баллов к вашему рейтингу. Каждый совет имеет значение!", reply_markup=advice_menu)
        else:
            await message.answer(f"УПС, произошла ошибка: {user_advice_response}", reply_markup=advice_menu)
            
        await state.clear()  # Завершаем состояние
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=advice_menu)