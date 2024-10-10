from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from keyboards.admin_keyb import deny_access_menu
from handlers.register_handlers import new_users

from aiogram import Bot
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "no_access")
async def no_access(callback: CallbackQuery, bot: Bot):

    # Получаем ID администратора и ID сообщения, по которому кликнули
    admin_id = callback.from_user.id
    message_id = callback.message.message_id

    # Редактируем текущее сообщение, заменяя только клавиатуру
    await bot.edit_message_reply_markup(chat_id=admin_id, message_id=message_id, reply_markup=deny_access_menu)
    await callback.answer()

@router.callback_query(F.data.startswith('deny_'))
async def deny_access_reason(callback: CallbackQuery, bot: Bot):

    # Получаем информацию о пользователе из контекста (например, через message или callback_data)
    current_message_id = callback.message.message_id - 1  # ID сообщения с запросом
    user_info = next((user for user in new_users if user['ID_message'] == current_message_id), None)

    # Проверка, найден ли пользователь
    if not user_info:
        await callback.message.answer("Пользователь для отказа не найден.")
        return

    user_id = user_info["ID_user"]
    
    # Определяем причину отказа
    if callback.data == "deny_format":
        reason = "Некорректный формат данных"
    elif callback.data == "deny_payment":
        reason = "Оплата не была получен."
    elif callback.data == "deny_fraud":
        reason = "Подозрение на мошенничество"
    elif callback.data == "deny_payment_no_enough":
        reason = "Оплата была получена не в полном объёме"
    
    # Отправляем сообщение пользователю
    new_users.remove(user_info)
    await bot.send_message(
        user_id,
        f"Ваш доступ к платформе StudyBoost был отклонен по следующей причине: {reason} ❌"
    )

    # Подтверждаем действие администратору
    await callback.message.answer(f"Вы отклонили доступ пользователю с ID: {user_id} по причине: {reason} ❌")
    await callback.message.edit_reply_markup(reply_markup=None)
