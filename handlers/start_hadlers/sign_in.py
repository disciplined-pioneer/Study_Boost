from config import ADMIN_ID
from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from states.payment_state import PaymentStates

from keyboards.admin_keyb import access_keyboard
from keyboards.platform_keyb import platform_menu
from handlers.start_hadlers.register_handlers import new_users

from states.payment_state import PaymentStates
from database.requests.user_access import can_use_feature
from handlers.commands_handlers.commands_handlers import user_subscription

router = Router()

@router.message(F.text == 'Войти в систему 🚪')
async def login_handler(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    can_use, _ = await can_use_feature(user_id)

    if can_use == 2:
        message_text = 'Добро пожаловать! Доступ к платформе открыт <u><b>без всяких ограничений</b></u> 😊'
    elif can_use == 1:
        message_text = 'Добро пожаловать! Ваша <u><b>подписка истекла</b></u>, и доступен только ограниченный функционал 🙂'
    else:
        message_text = 'Добро пожаловать! Вам доступен только <u><b>ограниченный функционал</b></u> 🙂'

    await message.reply(message_text, reply_markup=platform_menu, parse_mode="HTML")
