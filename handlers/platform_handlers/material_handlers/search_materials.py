from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database.requests.user_access import can_use_feature

from keyboards.material_keyb import search_materials

router = Router()

# Обработчик нажатия на кнопку "Поиск материалов 🔍"
@router.message(F.text == 'Поиск материалов 🔍')
async def view_categories(message: Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply("По каким категорияи вы хотите провести поиск:", reply_markup=search_materials)
    else:
        await message.answer(response_message)