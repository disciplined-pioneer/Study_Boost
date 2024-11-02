from aiogram import types
from aiogram import Router, F
from aiogram.types import Message
from handlers.commands_handlers.commands_handlers import get_top_10_users

router = Router()

@router.message(lambda message: message.text == '/top_users')
async def top_users(message: Message):
    # Получаем топ-10 пользователей
    top_users = await get_top_10_users()
    
    # Создаем красивый текст для вывода
    if not top_users:
        text = "🥇 Пока нет данных о рейтинге за текущий месяц."
    else:
        text = "🏆 <b>Топ 10 пользователей с самым большим рейтингом за этот месяц</b>:\n\n"
        for i, (user_id, rating) in enumerate(top_users, start=1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "⭐️"
            text += f"{medal} <b>Место {i}:</b> Пользователь ID: {user_id} — Рейтинг: <b>{rating:.1f}</b>\n"

    # Отправляем сообщение
    await message.answer(text, parse_mode="HTML")

