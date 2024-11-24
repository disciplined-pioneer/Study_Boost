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
        [KeyboardButton(text='Лекция 📚')],
        [KeyboardButton(text='Домашняя работа 🏠')],
        [KeyboardButton(text='Контрольная работа 📝')],
        [KeyboardButton(text='Лабораторная работа 🔬')],
        [KeyboardButton(text='Отменить состояние ❌')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

view_type_material = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Лекции 📚', callback_data='lecture')],
        [InlineKeyboardButton(text='Домашние работы 🏠', callback_data='homework')],
        [InlineKeyboardButton(text='Контрольные работы 📝', callback_data='test')],
        [InlineKeyboardButton(text='Лабораторные работы 🔬', callback_data='laboratory_work')],
    ]
)

grade_material_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👍', callback_data='like_material'), InlineKeyboardButton(text='👎', callback_data='dislike_material')]
    ]
)