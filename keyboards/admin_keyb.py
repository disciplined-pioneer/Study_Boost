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
        [InlineKeyboardButton(text='Three-Month Subscription', callback_data='subscription_three_month')],
        [InlineKeyboardButton(text='Basic Two-Month Subscription', callback_data='subscription_basic_two_month')],
        [InlineKeyboardButton(text='Basic Monthly Subscription', callback_data='subscription_basic_month')],
        [InlineKeyboardButton(text='Отказать в доступе ❌', callback_data='no_access')]
    ]
)

subscription_menu_two = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Unlimited', callback_data='subscription_unlimited')],
        [InlineKeyboardButton(text='Three-Month Subscription', callback_data='subscription_three_month')],
        [InlineKeyboardButton(text='Basic Two-Month Subscription', callback_data='subscription_basic_two_month')],
        [InlineKeyboardButton(text='Basic Monthly Subscription', callback_data='subscription_basic_month')],
        [InlineKeyboardButton(text='Отказать в доступе ❌', callback_data='no_access')]
    ]
)

# Клавиатура с причинами отказа
deny_access_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Некорректный формат данных", callback_data="deny_format")],
    [InlineKeyboardButton(text="Оплата не была получена", callback_data="deny_payment")],
    [InlineKeyboardButton(text="Подозрение на мошенничество", callback_data="deny_fraud")],
    [InlineKeyboardButton(text="Оплата была получена не в полном объёме", callback_data="deny_payment_no_enough")],
    [InlineKeyboardButton(text="Предоставить доступ ✅", callback_data="access")]
])