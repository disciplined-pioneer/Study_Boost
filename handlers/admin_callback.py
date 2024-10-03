from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from keyboards.admin_keyb import subscription_menu, access_keyboard
from handlers.register_handlers import new_users

from keyboards.platform_keyb import platform_menu

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
    subscription_type = callback.data.replace('subscription_', '').replace('_', ' ').title()
    
    # Получаем ID текущего сообщения
    current_message_id = callback.message.message_id - 1
    print(new_users)
    if not new_users:
        await callback.message.answer("Нет пользователей, ожидающих подписку.")
        return

    # Находим нужного пользователя по id сообщения
    user_id = None
    for i in range(len(new_users)):
        if new_users[i]['ID_message'] == current_message_id:
            user_info = new_users.pop(i)  # Удаляем пользователя из списка
            user_id = user_info.get("ID_user")
            break

    # Проверка, найден ли пользователь
    if user_id is None:
        await callback.message.answer("Пользователь для данной подписки не найден.")
        return
    
    # Отправляем уведомление пользователю ( и администратору  )и добавляем меню `platform_menu`
    await bot.send_message(
        user_id,
        f"Вам был предоставлен доступ к платформе StudyBoost с подпиской: {subscription_type}! ✅",
        reply_markup=platform_menu  # Отправляем сообщение вместе с клавиатурой platform_menu
    )

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
