from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

access_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Предоставить доступ ✅', callback_data='access')],
        [InlineKeyboardButton(text='Отказать в доступе ❌', callback_data='no_access')]
    ]
)

# Меню для выбора типа подписки
subscription_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Unlimited', callback_data='subscription_unlimited')],
        [InlineKeyboardButton(text='Premium', callback_data='subscription_premium')],
        [InlineKeyboardButton(text='Basic Monthly Subscription', callback_data='subscription_basic_month')],
        [InlineKeyboardButton(text='Basic Two-Month Access', callback_data='subscription_basic_two_month')],
        [InlineKeyboardButton(text='Three-Month Package', callback_data='subscription_three_month')],
        [InlineKeyboardButton(text='Назад 🔙', callback_data='back_to_access')]
    ]
)
