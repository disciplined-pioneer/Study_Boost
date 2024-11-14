from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

material_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить материал ➕')],
        [KeyboardButton(text='Просмотреть категории 📁')],
        [KeyboardButton(text='Поиск материалов 🔍')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)