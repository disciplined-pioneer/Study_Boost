from aiogram import types
from aiogram.types import Message
from aiogram import Router, F
from keyboards.platform_keyb import platform_menu, category_keyboard

from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.adviсe_states import AdviсeStates

from database.requests.user_access import can_use_feature

router = Router()

@router.message(F.text == 'Добавить совет ➕')
async def start_add(message: Message, state: FSMContext):
    await message.reply("Пожалуйста, выберите категорию:", reply_markup=category_keyboard)

# Обработчик нажатия на кнопку инлайн-клавиатуры
@router.callback_query()
async def category_selected(callback: CallbackQuery, state: FSMContext):

    # Сохранение выбранной категории в состояние
    selected_category = callback.data
    await state.update_data(selected_category=selected_category)
    
    # Ответ пользователю и завершение обработки
    await callback.message.reply("Пожалуйста, введите текст вашего совета:")
    await callback.answer()
    await state.set_state(AdviсeStates.category_advice)

# Текст совета
@router.message(F.text, AdviсeStates.category_advice)
async def process_advice(message: Message, state: FSMContext):
    data = await state.get_data()  # Получаем данные состояния
    selected_category = data.get("selected_category")  # Извлекаем выбранную категорию

    await state.update_data(category_advice=message.text)
    await message.answer(f"Ваш совет с текстом: '{message.text}' в категории '{selected_category}' был сохранён!")

    await state.clear()  # Завершаем состояние



@router.message(F.text == "Назад 🔙")
async def back_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Вы вернулись в главное меню 😊', reply_markup=platform_menu)
    else:
        await message.answer(response_message)