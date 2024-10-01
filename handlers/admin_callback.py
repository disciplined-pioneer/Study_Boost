from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from aiogram.fsm.context import FSMContext

from keyboards.admin_keyb import subscription_menu, access_keyboard
from handlers.register_handlers import new_users

router = Router()

@router.callback_query(F.data == "access")
async def access(callback: CallbackQuery, bot: Bot):
    admin_id = callback.from_user.id  # Получаем ID админа
    print(f"данные пользователя: {new_users}")

    # Отправляем меню для выбора типа подписки
    await bot.send_message(admin_id, "Выберите тип подписки:", reply_markup=subscription_menu)
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data.startswith('subscription_'))
async def subscription_choice(callback: CallbackQuery, bot: Bot):
    # Получаем данные из callback, чтобы определить выбранную подписку
    subscription_type = callback.data.replace('subscription_', '').replace('_', ' ').title()  # Преобразуем в читаемый формат

    # Проверяем, есть ли пользователи в списке
    if not new_users:
        await callback.message.answer("Нет пользователей, ожидающих подписку.")
        return

    # Берем первого пользователя в списке для предоставления подписки (можно доработать выбор по логике)
    user_info = new_users.pop(0)  # Удаляем пользователя и сохраняем его данные
    user_id = user_info.get("ID пользователя")

    if user_id:
        # Отправляем уведомление пользователю
        await bot.send_message(user_id, f"Вам был предоставлен доступ к платформе StudyBoost с подпиской: {subscription_type}! ✅")
        
        # Уведомляем администратора
        await callback.message.answer(f"Вы предоставили доступ пользователю с ID: {user_id} ✅")
    else:
        await callback.message.answer(f"Ошибка: не удалось найти ID пользователя.")
    
    await callback.message.edit_reply_markup(reply_markup=None)  # Очищаем клавиатуру после действия

# Кнопка "Назад"
@router.callback_query(F.data == "back_to_access")
async def back_to_access(callback: CallbackQuery):
    await callback.answer("Возвращаемся к доступу.")
    await callback.message.edit_text("Что вы хотите сделать?", reply_markup=access_keyboard)








@router.callback_query(F.data == "no_access")
async def no_access(callback: CallbackQuery, bot: Bot):
    admin_id = callback.from_user.id  # Получаем ID пользователя
    await callback.answer("В доступе отказано")
    await callback.message.edit_reply_markup(reply_markup=None)

    # Уведомляем о отказе доступа
    await bot.send_message(admin_id, 'В доступе было отказано ❌'
                                    '\nПожалуйста, попробуйте ещё раз')
    await callback.message.answer(f"Вы не предоставили доступ пользователю с ID: {admin_id} ❌")
