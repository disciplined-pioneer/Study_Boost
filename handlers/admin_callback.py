from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

router = Router()

@router.callback_query(F.data == "access")
async def access(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id  # Получаем ID пользователя
    await callback.answer("Доступ разрешён")
    
    # Уведомляем о предоставлении доступа
    await callback.message.answer(f"Вы предоставили доступ пользователю с ID: {user_id} ✅")
    await callback.message.edit_reply_markup(reply_markup=None)

    # Отправляем сообщение конкретному пользователю по его ID
    await bot.send_message(user_id, "Вам был доступ был предоставлен доступ к платформе StudyBoost_bot! ✅")  # Отправка сообщения конкретному пользователю

@router.callback_query(F.data == "no_access")
async def no_access(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id  # Получаем ID пользователя
    await callback.answer("В доступе отказано")
    await callback.message.edit_reply_markup(reply_markup=None)

    # Уведомляем о отказе доступа
    await bot.send_message(user_id, 'В доступе было отказано ❌'
                                    '\nПожалуйста, попробуйте ещё раз')
    await callback.message.answer(f"Вы не предоставили доступ пользователю с ID: {user_id} ❌")
