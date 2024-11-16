from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

material_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить материал ➕')],
        [KeyboardButton(text='Просмотреть категории 📁')],
        [KeyboardButton(text='Поиск материалов 🔍')],
        [KeyboardButton(text='Назад 🔙')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

type_material = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Лекция')],
        [KeyboardButton(text='Лабораторная работа')],
        [KeyboardButton(text='Модульный контроль')],
        [KeyboardButton(text='Отменить состояние ❌')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)