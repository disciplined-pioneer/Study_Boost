from datetime import datetime

from aiogram import types
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.adviсe_states import AdviсeStates
from database.handlers.database_handler import add_user_advice, add_user_rating
from keyboards.platform_keyb import platform_menu, category_keyboard
from database.requests.user_access import can_use_feature

router = Router()

@router.message(F.text == 'Добавить совет ➕')
async def start_add(message: Message, state: FSMContext):
    await message.reply("Пожалуйста, выберите категорию:", reply_markup=category_keyboard)

# Обработчик нажатия на кнопки инлайн-клавиатуры для добавления совета
@router.callback_query(lambda c: c.data in ['study', 'health', 'social', 'work'])
async def category_selected(callback: CallbackQuery, state: FSMContext):
    # Проверяем, в каком состоянии находимся
    current_state = await state.get_state()
    if current_state != AdviсeStates.category_advice:  # Только если состояние не 'category_advice'
        # Сохранение выбранной категории в состояние
        selected_category = callback.data
        await state.update_data(category_advice=selected_category)

        # Ответ пользователю и завершение обработки
        await callback.message.reply("Пожалуйста, введите текст вашего совета:")
        await callback.answer()
        await state.set_state(AdviсeStates.category_advice)
    else:
        await callback.answer("Сейчас нельзя выбрать категорию, завершите текущее действие.")


# Текст совета
@router.message(F.text, AdviсeStates.category_advice)
async def process_advice(message: Message, state: FSMContext):
    
    data = await state.get_data()  # Получаем данные состояния
    user_id = message.from_user.id

    # Добавляем оставшиеся данные
    await state.update_data(date_publication=datetime.now().date())
    await state.update_data(ID_user=user_id)
    await state.update_data(content=message.text)
    
    # Сохраняем данные в БД
    data = data = await state.get_data()
    user_advice_response = await add_user_advice(ID_user=data.get('ID_user'),
                          date_publication=data.get('date_publication'),
                          content=data.get('content'),
                          type_advice=data.get('category_advice'),
                          grade_advice='0')
    if user_advice_response == "Совет пользователя успешно добавлен!":
        await add_user_rating(user_id)
        await message.answer(f"Спасибо за ваш вклад! Ваш совет был добавлен, и вы получили +0.5 баллов к вашему рейтингу. Каждый совет имеет значение!")
    else:
        await message.answer(f"УПС, произошла ошибка: {user_advice_response}")
    await state.clear()  # Завершаем состояние


@router.message(F.text == "Назад 🔙")
async def back_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Вы вернулись в главное меню 😊', reply_markup=platform_menu)
    else:
        await message.answer(response_message)