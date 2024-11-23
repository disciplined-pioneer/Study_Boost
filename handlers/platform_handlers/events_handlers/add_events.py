from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.events_state import EventsStates
from keyboards.events_keyb import events_menu
from keyboards.cancellation_states import cancel_state

from database.handlers.database_handler import add_event
from database.requests.user_access import can_use_feature
from NI_assistants.sentiment_text import analyze_sentiment

router = Router()

# Обработчик для начала добавления мероприятия
@router.message(F.text == 'Добавить мероприятие ➕')
async def start_add_event(message: Message, state: FSMContext):
    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)
    
    if can_use:
        await state.update_data(ID_user=user_id, date_publication=datetime.now().date())
        await message.reply(
            "📅 <b>Введите дату проведения мероприятия</b>\n\n"
            "Пожалуйста, укажите дату в формате <b>ГГГГ-ММ-ДД</b> (например, 2024-12-10).\n"
            "Это поможет участникам заранее спланировать своё время и подготовиться к вашему событию! 🗓️",
            parse_mode="HTML",
            reply_markup=cancel_state
        )
        await state.set_state(EventsStates.date)
    else:
        await message.answer(response_message)

# Обработчик для даты мероприятия
@router.message(EventsStates.date)
async def process_event_date(message: Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить ❌']:
        try:
            event_date = datetime.strptime(message.text, "%Y-%m-%d").date()
            await state.update_data(date=event_date)
            await message.reply(
                "📍 <b>Введите место проведения мероприятия</b>\n\n"
                "Укажите адрес или место, где пройдет мероприятие. Если возможно, добавьте ориентиры или информацию о том, как добраться.\n"
                "Чем точнее будут указания, тем легче будет участникам найти локацию! 🗺️",
                parse_mode="HTML",
                reply_markup=cancel_state
            )
            await state.set_state(EventsStates.place)
        except ValueError:
            await message.reply("Неверный формат даты 🛑\nПопробуйте снова", reply_markup=events_menu)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=events_menu)

# Обработчик для места проведения
@router.message(EventsStates.place)
async def process_place(message: Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить ❌']:
        place = message.text.strip()
        if place:

            # Проверка качества текста
            sentiment_score = await analyze_sentiment(message.text)
            if sentiment_score <= -0.01:
                await message.answer("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст", reply_markup=events_menu)
                return
            else:
                await state.update_data(place=place)
                await message.reply(
                    "🕒 <b>Введите время проведения мероприятия</b>\n\n"
                    "Укажите время начала мероприятия в формате <b>ЧЧ:ММ</b> (например, 15:30).\n",
                    parse_mode="HTML",
                    reply_markup=cancel_state
                )
                await state.set_state(EventsStates.time)
        else:
            await message.reply("Место не может быть пустым 🛑\nПопробуйте снова", reply_markup=events_menu)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=events_menu)

# Обработчик для времени мероприятия
@router.message(EventsStates.time)
async def process_event_time(message: Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить ❌']:
        try:
            # Преобразуем время в строку для совместимости с SQLite
            event_time = datetime.strptime(message.text, "%H:%M").time().strftime("%H:%M")
            await state.update_data(time=event_time)

            await message.reply(
                "Пожалуйста, введите описание вашего мероприятия. Укажите:\n"
                "• Кого ждёте и кто может участвовать?\n"
                "• Что будет происходить на мероприятии?\n"
                "• Нужно ли что-то взять с собой?\n"
                "• Особые условия или важные детали.\n\n"
                "Чем подробнее будет описание, тем легче участникам понять, подходит ли им ваше мероприятие! 😊",
                parse_mode="HTML",
                reply_markup=cancel_state
            )

            await state.set_state(EventsStates.description)
        except ValueError:
            await message.reply("Неверный формат времени 🛑\nПопробуйте снова", reply_markup=events_menu)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=events_menu)

# Обработчик для описания и сохранения данных
@router.message(EventsStates.description)
async def process_description(message: Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить ❌']:
    
        description = message.text.strip()
        if description:

            # Проверка качества текста
            sentiment_score = await analyze_sentiment(message.text)
            if sentiment_score <= -0.01:
                await message.answer("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст", reply_markup=events_menu)
                return
            
            else:
                data = await state.get_data()

                # Записываем данные в БД
                await add_event(
                    ID_user=data['ID_user'],
                    date_publication=data['date_publication'],
                    place=data['place'],
                    event_date=data['date'],
                    event_time=data['time'],  # event_time теперь строка
                    description=description
                )
                await message.reply(
                    "✅ <b>Мероприятие успешно добавлено!</b>\n\n"
                    "Спасибо за регистрацию мероприятия! 🎉\n"
                    "Теперь участники смогут узнать о вашем событии и присоединиться. Удачи в организации! 🥳",
                    parse_mode="HTML",
                    reply_markup=events_menu
                )
                await state.clear()
        else:
            await message.reply("Описание не может быть пустым 🛑\nПопробуйте снова", reply_markup=events_menu)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=events_menu)