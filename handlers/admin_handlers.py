from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from handlers.register_handlers import new_users
from config import ADMIN_ID

router = Router()

def access_keyboard(user_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Дать доступ",
                    callback_data=f"grant_{user_id}"
                ),
                InlineKeyboardButton(
                    text="Не дать доступ",
                    callback_data=f"deny_{user_id}"
                )
            ]
        ]
    )

@router.callback_query(F.data.startswith("grant_"))
async def grant_access_callback(call: CallbackQuery):
    user_id = call.data.split("_")[1]
    
    user_info = next((user for user in new_users if str(user['ID пользователя']) == user_id), None)
    if user_info:
        new_users.remove(user_info)

        # Уведомление пользователя
        await call.bot.send_message(user_id, "Поздравляем! Вам был предоставлен доступ к @StudyBoost_bot.")
        await call.answer("Доступ предоставлен!")

@router.callback_query(F.data.startswith("deny_"))
async def deny_access_callback(call: CallbackQuery):
    user_id = call.data.split("_")[1]

    user_info = next((user for user in new_users if str(user['ID пользователя']) == user_id), None)
    if user_info:
        new_users.remove(user_info)

        # Уведомление пользователя
        await call.bot.send_message(user_id, "К сожалению, вам было отказано в доступе к @StudyBoost_bot.")
        await call.answer("Доступ не предоставлен!")
