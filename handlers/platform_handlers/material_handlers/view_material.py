from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.material_keyb import view_type_material

from database.requests.user_access import can_use_feature

router = Router()

# Обработчик нажатия на кнопку "Просмотреть категории"
@router.message(F.text == 'Просмотреть категории 📁')
async def view_categories(message: Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply("Пожалуйста, выберите категорию:", reply_markup=view_type_material)
    else:
        await message.answer(response_message)