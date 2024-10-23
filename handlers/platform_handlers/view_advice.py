from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from database.requests.random_advice import get_random_advice, get_user_name
from keyboards.platform_keyb import view_category_keyboard

from keyboards.platform_keyb import grade_keyboard

router = Router()

# Обработчик нажатия на кнопку "Просмотреть категории 🗂"
@router.message(F.text == 'Просмотреть категории 🗂')
async def view_categories(message: Message):
    await message.reply("Пожалуйста, выберите категорию:", reply_markup=view_category_keyboard)

# Обработчик нажатия на кнопки для просмотра советов
@router.callback_query(lambda c: c.data.startswith('view_'))
async def process_callback_advice(callback_query: CallbackQuery):
    advice_type = callback_query.data.split('_')[1]  # Получаем тип совета из callback_data

    # Получаем случайный совет по выбранной категории
    random_advice, user_id = await get_random_advice(advice_type)
    if random_advice == "К сожалению, нет доступных советов по этой категории":
        await callback_query.message.answer("К сожалению, нет доступных советов по этой категории")
    else:
        user_name = await get_user_name(user_id)  # Получаем имя пользователя, который дал совет
        if user_name:
            await callback_query.message.answer(f"Совет от {user_name}: \n✍️ «{random_advice}»\n\n🎯 Какую оценку вы дадите этому совету? Оставьте свою оценку ниже!", reply_markup=grade_keyboard)
    await callback_query.answer()
