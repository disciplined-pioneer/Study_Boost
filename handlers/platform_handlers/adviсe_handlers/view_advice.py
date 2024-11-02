import re
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.platform_keyb import grade_keyboard
from keyboards.platform_keyb import view_category_keyboard

from database.requests.advice import get_random_advice
from database.requests.user_access import can_use_feature
from database.requests.advice import check_rating_history
from database.handlers.database_handler import add_user_rating_history
from database.handlers.advice_handler import like_advice, dislike_advice

router = Router()

# Обработчик нажатия на кнопку "Просмотреть категории"
@router.message(F.text == 'Просмотреть категории 🗂')
async def view_categories(message: Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply("Пожалуйста, выберите категорию:", reply_markup=view_category_keyboard)
    else:
        await message.answer(response_message)

# Обработчик нажатия на кнопки для просмотра советов
@router.callback_query(lambda c: c.data.startswith('view_'))
async def process_callback_advice(callback_query: CallbackQuery):
    advice_type = callback_query.data.split('_')[1]  # Получаем тип совета из callback_data

    # Получаем случайный совет по выбранной категории
    random_advice = await get_random_advice(advice_type)
    if random_advice is None:  # Проверяем, что совет не найден
        await callback_query.message.answer("К сожалению, нет доступных советов по этой категории")
    else:
        await callback_query.message.answer(
            f"Совет №{random_advice['advice_id']} от пользователя ID_{random_advice['ID_user']}: \n✍️ «{random_advice['content']}»\n\nРейтинг совета: {random_advice['like_advice']} 👍 | 👎 {random_advice['dislike_advice']}",
            reply_markup=grade_keyboard
        )
    await callback_query.answer()

# Обработчик нажатия на кнопки для лайка и дизлайка
@router.callback_query(lambda c: c.data in ['like', 'dislike'])
async def process_rating_callback(callback_query: CallbackQuery):
    action_type = callback_query.data  # Получаем тип действия: "like" или "dislike"
    accrual_date = datetime.now().date()
    rating_value = '1' if action_type == 'like' else '-1'  # Начисляем +1 за лайк и -1 за дизлайк

    # Используем регулярное выражение для поиска ID и номера совета
    message_text = callback_query.message.text
    match_id = re.search(r'ID_(\d+)', message_text)
    match_advice_number = re.search(r"Совет №(\d+)", message_text)

    # Обрабатываем действие пользователя
    user_id = int(match_id.group(1))  # Преобразуем ID в целое число
    advice_number = int(match_advice_number.group(1))  # Преобразуем номер совета в целое число
    result = await check_rating_history(advice_number, callback_query.from_user.id)

    if result:
       
        # Добавляем рейтинг пользователю, который опубликовал совет
        await add_user_rating_history(
            advice_id=advice_number,
            id_user=user_id,
            granted_by=callback_query.from_user.id,
            accrual_date=accrual_date,
            action_type=action_type + '_advice',
            rating_value=rating_value
        )

        # Добавлеяем лайк или дизлайк на совет
        if action_type == "like":
            await like_advice(advice_number)
        if action_type == "dislike":
            await dislike_advice(advice_number)

        # Отправляем сообщение пользователю, который опубликовал совет
        await callback_query.bot.send_message(
            chat_id=user_id,
            text=f"Вы получили {'лайк' if action_type == 'like' else 'дизлайк'} от пользователя ID_{callback_query.from_user.id}!"
        )
    else:
        await callback_query.answer(f"Вы уже оставляли свой отзыв для этого совета!")
    
    if callback_query.message.reply_markup:
        await callback_query.message.edit_reply_markup()