from datetime import datetime, timedelta
import aiosqlite

async def get_events_by_period(period: str):
    database_path = 'database/data/events.db'
    today = datetime.now().date()

    # Определяем конечную дату выборки на основе выбранного периода
    if period == 'неделя':
        end_date = today + timedelta(weeks=1)
    elif period == '2 недели':
        end_date = today + timedelta(weeks=2)
    elif period == 'месяц':
        end_date = today + timedelta(weeks=4)
    elif period == '2 месяца':
        end_date = today + timedelta(weeks=8)
    else:
        return "Некорректный период."

    # Запрос к базе данных для получения мероприятий в выбранный период
    async with aiosqlite.connect(database_path) as db:
        cursor = await db.execute('''
            SELECT * FROM events
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
        ''', (today, end_date))
        
        events = await cursor.fetchall()
        await cursor.close()

    # Формируем текст для отправки с использованием HTML-форматирования
    if events:
        events_text = "\n\n".join(
            f"🎉 <b>Мероприятие №{event[0]}</b>\n"
            f"📅 <b>Дата проведения:</b> {event[4]}\n"
            f"⏰ <b>Время:</b> {event[5]}\n"
            f"📍 <b>Место:</b> {event[3]}\n"
            f"📝 <b>Описание:</b> {event[6]}\n"
            "─────────────────────"
            for event in events
        )
    else:
        events_text = "Мероприятий за выбранный период нет"

    return events_text
