from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from keyboards.admin_keyb import subscription_menu
from handlers.register_handlers import new_users

from keyboards.platform_keyb import platform_menu

import os
from database.handlers.database_create import create_db
from database.handlers.database_handler import register_user
from database.handlers.print_db import print_all_users


router = Router()

@router.callback_query(F.data == "access")
async def access(callback: CallbackQuery, bot: Bot):

    # Получаем ID администратора и ID сообщения, по которому кликнули
    admin_id = callback.from_user.id
    message_id = callback.message.message_id

    # Редактируем текущее сообщение, заменяя только клавиатуру
    await bot.edit_message_reply_markup(chat_id=admin_id, message_id=message_id, reply_markup=subscription_menu)
    await callback.answer()

# определение подписки
@router.callback_query(F.data.startswith('subscription_'))
async def subscription_choice(callback: CallbackQuery, bot: Bot):

    # Получаем выбранный тип подписки из данных callback
    subscription_type = callback.data.replace('subscription_', '').replace('_', ' ').title()
    
    # Получаем ID текущего сообщения и ищем пользователя
    current_message_id = callback.message.message_id - 1
    user_info = next((user for user in new_users if user['ID_message'] == current_message_id), None)

    # Проверка, найден ли пользователь
    if not user_info:
        await callback.message.answer("Пользователь для данной подписки не найден.")
        return

    user_id = user_info["ID_user"]

    # Обновляем данные пользователя и регистрируем его в БД
    user_info['subscription_type'] = subscription_type
    db_dir = 'database/data'
    os.makedirs(db_dir, exist_ok=True)
    database = os.path.join(db_dir, 'users.db') 
    
    await create_db(database)
    await register_user(user_info, database)
    #await print_all_users(database)
    new_users.remove(user_info)

    # Отправляем уведомление пользователю и добавляем меню `platform_menu`
    await bot.send_message(
        user_id,
        f"Вам был предоставлен доступ к платформе StudyBoost с подпиской: {subscription_type}! ✅",
        reply_markup=platform_menu
    )

    # Подтверждаем действие администратору
    await callback.message.answer(f"Вы предоставили доступ пользователю с ID: {user_id} ✅")
    await callback.message.edit_reply_markup(reply_markup=None)





@router.callback_query(F.data == "no_access")
async def no_access(callback: CallbackQuery, bot: Bot):
    admin_id = callback.from_user.id
    await callback.answer("В доступе отказано")
    await callback.message.edit_reply_markup(reply_markup=None)

    # Уведомляем о отказе доступа
    await bot.send_message(admin_id, 'В доступе было отказано ❌'
                                    '\nПожалуйста, попробуйте ещё раз')
    await callback.message.answer(f"Вы не предоставили доступ пользователю с ID: {admin_id} ❌")
