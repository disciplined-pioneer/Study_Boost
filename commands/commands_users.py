from datetime import datetime

from aiogram import Router
from aiogram.types import Message

from keyboards.registration_keyb import registration_menu
from database.requests.user_search import count_referrals
from handlers.commands_handlers.commands_handlers import user_rating, fetch_user_data, get_top_10_users, user_subscription, payment_information

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

# Вывод количества рефералом пользователя
@router.message(lambda message: message.text == '/my_referal')
async def referral_handler(message: Message):
    user_id = message.from_user.id
    referral_count = await count_referrals(user_id)  # Функция для подсчета рефералов
    
    await message.answer(
        f"👥 <b>Количество ваших рефералов на данный момент:</b> <u>{referral_count}</u>\n\n"
        "📢 <b>Преимущества реферальной программы:</b>\n\n"
        "1️⃣ За каждого нового реферала вы получаете <b>+5 баллов</b> к вашему рейтингу 📈\n"
        f"2️⃣ Если вы приведёте <b>10 пользователей</b>, подписка для вас станет <b>бесплатной НАВСЕГДА</b> 🆓\n\n"
        "💡 <i>Приглашайте друзей и повышайте свой рейтинг, чтобы открыть все преимущества!</i>"
    , parse_mode="HTML")

# Вывод инфомрмации о подписке
@router.message(lambda message: message.text == '/subscription_status')
async def subscription_status(message: Message):

    # Определеяем тип подписки пользователя
    user_id = message.from_user.id
    subscription_data = await user_subscription(user_id)
    
    # Если подписка не найдена
    if not subscription_data:
        await message.answer("Вы не были найден в базе данных. Пожалуйста, пройдите регистрацию")
        return

    # Получаем статус подписки
    subscription_status = subscription_data[0]
    payment_data = await payment_information(user_id)

    # Если информация об оплате не найдена
    if not payment_data:
        await message.answer("Информация о вашей оплате не найдена. Пожалуйста, свяжитесь с поддержкой")
        return

    # Получаем дату оплаты и окончания подписки
    payment_date = datetime.strptime(payment_data[0], '%Y-%m-%d').date()
    expiration_date = datetime.strptime(payment_data[1], '%Y-%m-%d').date()
    days_left = (expiration_date - datetime.now().date()).days

    # Формируем сообщение для пользователя
    response_message = (
        f"🔔 <b>Статус подписки:</b> {subscription_status}\n"
        f"💵 <b>Дата оплаты:</b> {payment_date.strftime('%d.%m.%Y')}\n"
        f"📅 <b>Дата окончания:</b> {expiration_date.strftime('%d.%m.%Y')}\n"
        f"⏳ <b>Осталось дней до окончания:</b> {days_left} дней"
    )

    await message.answer(response_message, parse_mode='HTML')

# Вывод реферальной ссылки
@router.message(lambda message: message.text == '/cancellation')
async def cancellation_handler(message: Message):
    await message.answer(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=registration_menu
        )