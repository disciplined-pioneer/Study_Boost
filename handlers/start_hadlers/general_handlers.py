import time

from aiogram import Router, F
from aiogram.types import Message

from database.requests.user_search import count_users

router = Router()

@router.message(F.text == 'Виды подписок 💵')
async def login_handler(message: Message):

    # Формируем базовый текст
    text = (
        "<b>🎉 Доступные подписки для @StudyBoost_bot</b>\n\n"
        "📅 <b>Basic Month:</b> подписка на 1 месяц — <b>50 ₽</b>\n\n"
        "📅 <b>Basic Two Month:</b> подписка на 2 месяца — <b>90 ₽</b> <i>(экономия 10%)</i>\n\n"
        "📅 <b>Three Month:</b> подписка на 3 месяца — <b>120 ₽</b> <i>(экономия 20%)</i>\n\n"
    )

    # Добавляем "Premium" только если пользователей <= 50
    user_count = await count_users()
    if user_count <= 50:
        text += "💎 <b>Premium:</b> пожизненная подписка за 25 ₽ для первых 50 пользователей\n\n"
    
    text += "📌 <b>Unlimited:</b> пожизненная подписка, доступная при регистрации 10 пользователей по вашей реферальной ссылке.\n\n"
    await message.reply(text, parse_mode="HTML")
    time.sleep(1)

    # Добавляем остальной текст
    text_card = (
        "🔓 Все пользователи имеют ограниченный функционал до оформления подписки. Подписка дает доступ к расширенным функциям и уникальным материалам.\n\n"
        'Для оформления подписки переведите соответствующую сумму на карту "КЛЕВЕР 🍀"\n\n'
        "🔗 Нажмите на номер, чтобы скопировать: <code>9104016039962016</code>"
    )

    # Отправляем сообщение
    await message.reply(text_card, parse_mode="HTML")

@router.message(F.text == 'Инструкция 📕')
async def instruction_handler(message: Message):

    # Отправляем документ
    await message.bot.send_document(
        chat_id=message.from_user.id,
        document='BQACAgIAAxkBAAJUSmdLKRRfEi3Z5x1zOtvmmlZRombTAAL6eAAC0zJYStiveZibQMF0NgQ',
        caption = f'Инструкция содержит подробное описание всех функций платформы, пошаговое руководство по регистрации и использованию бота, а также примеры обмена учебными материалами и заработка очков за активность',
    )

@router.message(F.text == 'Создатель ©️')
async def creator_handler(message: Message):
    text = (
        "Привет, Я Virtu! 👨‍💻\n\n"
        "Я являюсь разработчиком этого Telegram-бота и Python-разработчиком, специализирующимся на Data Science 🤖\n\n"
        "Моя цель — создавать полезные и удобные инструменты, которые помогут студентам эффективно обмениваться знаниями и учебными материалами 📚\n\n"
        "Я студент первого курса, и этот бот был разработан для того, чтобы упростить жизнь студентов. Если у вас есть идеи или предложения, буду рад их услышать! 😉\n\n"
        "Для вопросов или предложений вы можете связаться со мной через почту virtu1129@gmail.com  📩"
    )

    # ID фотографии
    photo_id = 'AgACAgIAAxkBAAIIg2b6x72lvUPWCK_udjCgFdxTAAHamQAC2usxG3jT2UuwWltlE_cjTgEAAwIAA3kAAzYE'
    await message.answer_photo(photo=photo_id, caption=text, parse_mode='Markdown')