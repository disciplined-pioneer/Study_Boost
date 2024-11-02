from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from handlers.commands_handlers.commands_handlers import user_rating
from handlers.commands_handlers.commands_handlers import fetch_user_data
from handlers.commands_handlers.commands_handlers import get_top_10_users

router = Router()

# Топ 10 пользователь с наибольшим рейтингом
@router.message(lambda message: message.text == '/top_users')
async def top_users(message: Message):
    # Получаем топ-10 пользователей
    top_users = await get_top_10_users()
    
    # Создаем красивый текст для вывода
    if not top_users:
        text = "🥇 Пока нет данных о рейтинге за текущий месяц"
    else:
        text = "🏆 <b>Топ 10 пользователей с самым большим рейтингом за этот месяц</b>:\n\n"
        for i, (user_id, rating) in enumerate(top_users, start=1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "⭐️"
            text += f"{medal} <b>Место {i}:</b> Пользователь ID: {user_id} — Рейтинг: <b>{rating:.1f}</b>\n"

    # Отправляем сообщение
    await message.answer(text, parse_mode="HTML")

# Вывод рейтинга пользователя
@router.message(lambda message: message.text == '/my_rating')
async def my_rating(message: Message):
    user_id = message.from_user.id
    rating = await user_rating(user_id)  # Получаем рейтинг пользователя

    # Форматируем сообщение
    if rating > 0:
        response = (
            f"🌟 <b>Ваш рейтинг за текущий месяц:</b> <b>{rating:.1f}</b>\n\n"
            "🎉 Поздравляем с вашими достижениями! Продолжайте в том же духе!"
        )
    else:
        response = (
            "❌ У вас пока нет рейтинга за текущий месяц\n\n"
            "💪 Не упустите возможность заработать баллы! Участвуйте в активности!"
        )

    await message.answer(response, parse_mode='HTML')

# Вывод информации о пользователе
@router.message(lambda message: message.text == '/my_data')
async def my_data(message: Message):
    user_id = message.from_user.id
    user_info = await fetch_user_data(user_id)

    if user_info:
        response_text = (
            f"👤 <b>Ваши данные:</b>\n"
            f"\n<b>ID пользователя:</b> {user_info['ID_user']}\n"
            f"\n<b>Telegram:</b> {user_info['telegram']}\n"
            f"\n<b>ID Реферала:</b> {user_info['referrer_id'] or 'Нет'}\n"
            f"\n<b>Имя:</b> {user_info['name_user']}\n"
            f"\n<b>Город университета:</b> {user_info['city_university'] or 'Не указано'}\n"
            f"\n<b>Название университета:</b> {user_info['name_university'] or 'Не указано'}\n"
            f"\n<b>Факультет:</b> {user_info['faculty'] or 'Не указано'}\n"
            f"\n<b>Курс:</b> {user_info['course'] or 'Не указано'}\n"
        )
    else:
        response_text = "❌ <b>Данные о пользователе не найдены.</b>"

    await message.answer(response_text, parse_mode='HTML')

# Вывод реферальной ссылки
@router.message(lambda message: message.text == '/referal_link')
async def referral_handler(message: Message):
    user_id = message.from_user.id  # Уникальный идентификатор пользователя
    referral_link = f"https://t.me/StudyBoost_bot?start={user_id}"
    
    await message.answer(
        f"🔗 <b>Ваша персональная реферальная ссылка:</b>\n{referral_link}\n\n"
        "💬 Отправьте эту ссылку своим друзьям! Если они перейдут по ней и начнут использовать бота, "
        "вы получите следующие бонусы:\n\n"
        "1️⃣ <b>+5 баллов к вашему рейтингу</b> за каждого нового реферала 📈\n"
        "2️⃣ <b>Бесплатная подписка НАВСЕГДА</b> при достижении 10 рефералов 🆓\n\n"
        "Станьте топ-пользователем и наслаждайтесь всеми преимуществами!"
    , parse_mode="HTML")