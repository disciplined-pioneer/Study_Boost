from aiogram import Router, F
from aiogram import types
from keyboards.platform_keyb import platform_menu

from database.requests.user_access import can_use_feature

router = Router()



@router.message(F.text == "Назад 🔙")
async def back_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Вы вернулись в главное меню', reply_markup=platform_menu)
    else:
        await message.answer(response_message)