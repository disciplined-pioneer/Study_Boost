from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.material_keyb import search_materials

from database.requests.user_access import can_use_feature

from handlers.platform_handlers.material_handlers.search_type_material import get_material_ids_by_type

router = Router()

# Обработчик нажатия на кнопку "Просмотреть категории"
@router.message(F.text == 'Просмотреть категории 📁')
async def view_categories(message: Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply("Пожалуйста, выберите категорию по которой хотите провести поиск", reply_markup=search_materials)
    else:
        await message.answer(response_message)

# Дополнение к вашему обработчику
@router.callback_query(F.data.in_({'lecture', 'homework', 'test', 'laboratory_work'}))
async def handle_material_type(callback: CallbackQuery):

    material_type = str(callback.data)
    material_ids = await get_material_ids_by_type(material_type)

    if material_ids:
        material_list = '\n'.join(map(str, material_ids))
        await callback.message.answer(f"Материалы для категории {material_type}:\n{material_list}")
    else:
        await callback.message.answer(f"Материалы для категории {material_type} отсутствуют.")

    await callback.answer()

