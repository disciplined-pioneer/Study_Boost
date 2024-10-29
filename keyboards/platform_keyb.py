from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

platform_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Советы 🦉')],
        [KeyboardButton(text='Материалы 📔')],
        [KeyboardButton(text='Мероприятия 🎉')],
        [KeyboardButton(text='...')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

adviсe_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Добавить совет ➕'), KeyboardButton(text='Назад 🔙')],
        [KeyboardButton(text='Учёба и успеваемость 👨🏻‍🏫')],
        [KeyboardButton(text='Здоровье и благополучие ❤️')],
        [KeyboardButton(text='Социальная жизнь 🧍')],
        [KeyboardButton(text='Работа и карьера 💼')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)