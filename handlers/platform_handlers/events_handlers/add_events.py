from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.events_state import EventsStates

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
        # Установим дату публикации сразу, так как она текущая
        await state.update_data(ID_user=user_id, date_publication=datetime.now().date())
        await message.reply("Введите дату проведения мероприятия (например, 2024-12-10):")
        await state.set_state(EventsStates.date)
    else:
        await message.answer(response_message)

# Обработчик для даты мероприятия
@router.message(EventsStates.date)
async def process_event_date(message: Message, state: FSMContext):
    try:
        event_date = datetime.strptime(message.text, "%Y-%m-%d").date()
        await state.update_data(date=event_date)
        await message.reply("Введите место проведения мероприятия:")
        await state.set_state(EventsStates.place)
    except ValueError:
        await message.reply("Неверный формат даты. Попробуйте снова.")
        await state.clear()

# Обработчик для места проведения
@router.message(EventsStates.place)
async def process_place(message: Message, state: FSMContext):

    place = message.text.strip()
    if place:

        # Проверка качества текста
        sentiment_score = await analyze_sentiment(message.text)
        if sentiment_score <= -0.01:
            await message.answer("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            await state.clear()  # Завершаем состояние
            return
        else:
            await state.update_data(place=place)
            await message.reply("Введите время проведения мероприятия (например, 15:30):")
            await state.set_state(EventsStates.time)
    else:
        await message.reply("Место не может быть пустым.")
        await state.clear()

# Обработчик для времени мероприятия
@router.message(EventsStates.time)
async def process_event_time(message: Message, state: FSMContext):
    try:
        # Преобразуем время в строку для совместимости с SQLite
        event_time = datetime.strptime(message.text, "%H:%M").time().strftime("%H:%M")
        await state.update_data(time=event_time)
        await message.reply("Введите описание мероприятия:")
        await state.set_state(EventsStates.description)
    except ValueError:
        await message.reply("Неверный формат времени. Попробуйте снова.")
        await state.clear()

# Обработчик для описания и сохранения данных
@router.message(EventsStates.description)
async def process_description(message: Message, state: FSMContext):
    
    description = message.text.strip()
    if description:

        # Проверка качества текста
        sentiment_score = await analyze_sentiment(message.text)
        if sentiment_score <= -0.01:
            await message.answer("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            await state.clear()  # Завершаем состояние
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
            await message.reply("Мероприятие успешно добавлено!")
            await state.clear()
    else:
        await message.reply("Описание не может быть пустым.")
        await state.clear()