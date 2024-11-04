from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

events_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📅 В ближайшую неделю'), 
            KeyboardButton(text='🗓️ В ближайшие 2 недели')
        ],
        [
            KeyboardButton(text='📆 В ближайший месяц'), 
            KeyboardButton(text='📅 В ближайшие 2 месяца')
        ],
        [KeyboardButton(text='Добавить мероприятие ➕')],
        [KeyboardButton(text='Назад 🔙')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)
