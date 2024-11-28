from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

platform_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Советы 🦉'), KeyboardButton(text='Материалы 📔')],
        [KeyboardButton(text='Мероприятия 🎉'), KeyboardButton(text='Настройки ⚙️')],
        [KeyboardButton(text='Меню оплаты ◀️')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Команды 📜'), KeyboardButton(text='Предложения ➕')],
        [KeyboardButton(text='Инструкция 📕'), KeyboardButton(text='Помощь ❓')], 
        [KeyboardButton(text='Назад 🔙')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)