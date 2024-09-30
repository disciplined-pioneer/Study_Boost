from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

access_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Предоставить доступ ✅', callback_data='access')],
        [InlineKeyboardButton(text='Отказать в доступе ❌', callback_data='no_access')]
    ]
)