from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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

search_materials = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='По курсам 📚', callback_data='search_by_courses')],
        [InlineKeyboardButton(text='По факультетам 🏫', callback_data='search_by_faculties')],
        [InlineKeyboardButton(text='По предметам 📖', callback_data='search_by_subjects')],
        [InlineKeyboardButton(text='По типу материала 📂', callback_data='search_by_material_type')],
    ]
)
