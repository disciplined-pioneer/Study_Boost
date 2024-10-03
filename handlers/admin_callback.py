from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from keyboards.admin_keyb import subscription_menu, access_keyboard
from keyboards.platform_keyb import platform_menu
from handlers.register_handlers import new_users

router = Router()

# Основное меню администрирования
@router.callback_query(F.data == "access")
async def access(callback: CallbackQuery, bot: Bot):
    admin_id = callback.from_user.id
    message_id = callback.message.message_id

    # Редактируем текущее сообщение, заменяя только клавиатуру
    await bot.edit_message_reply_markup(chat_id=admin_id, message_id=message_id, reply_markup=subscription_menu)
    await callback.answer()


# Определение подписки и добавление пользователя
@router.callback_query(F.data.startswith('subscription_'))
async def subscription_choice(callback: CallbackQuery, bot: Bot):
    subscription_type = callback.data.replace('subscription_', '').replace('_', ' ').title()
    current_message_id = callback.message.message_id

    if not new_users:
        await callback.message.answer("Нет пользователей, ожидающих подписку.")
        return

    user_id = None
    for i in range(len(new_users)):
        if new_users[i]['ID сообщения'] == current_message_id:
            user_info = new_users.pop(i)
            user_id = user_info.get("ID пользователя")
            break

    if user_id is None:
        await callback.message.answer("Пользователь для данной подписки не найден.")
        return

    # Отправляем уведомление пользователю с добавлением меню
    await bot.send_message(
        user_id,
        f"Вам был предоставлен доступ к платформе StudyBoost с подпиской: {subscription_type}! ✅",
        reply_markup=platform_menu
    )

    await callback.message.answer(f"Вы предоставили доступ пользователю с ID: {user_id} ✅")
    await callback.message.edit_reply_markup(reply_markup=None)


# Кнопка "Назад" для возврата в меню доступа
@router.callback_query(F.data == "back_to_access")
async def back_to_access(callback: CallbackQuery):
    await callback.answer("Возвращаемся к доступу.")
    await callback.message.edit_reply_markup(reply_markup=access_keyboard)
