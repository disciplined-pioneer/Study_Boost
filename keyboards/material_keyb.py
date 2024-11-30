from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

material_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить материал ➕')],
        [KeyboardButton(text='Поиск материалов 🔍')],
        [KeyboardButton(text='Назад 🔙')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

type_material = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Лекция 📚'), KeyboardButton(text='Семинар 🏫')],
        [KeyboardButton(text='Домашняя работа 🏠'), KeyboardButton(text='Лабораторная работа 🔬')],
        [KeyboardButton(text='Контрольная работа 📝'), KeyboardButton(text='Экзамен 📕')],
        [KeyboardButton(text='Отменить ❌')]
    ],
    resize_keyboard=True  # Компактная клавиатура
)

grade_material_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👍', callback_data='like_material'), InlineKeyboardButton(text='👎', callback_data='dislike_material')]
    ]
)