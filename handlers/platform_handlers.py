from aiogram import Router, F
from aiogram import types
from keyboards.platform_keyb import platform_menu, adviсe_menu

from database.requests.user_access import can_use_feature

router = Router()

@router.message(F.text == "Советы 🦉")
async def adviсe_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Пожалуйста, выберите категорию, из которой хотите получить совет, нажав на одну из кнопок ниже: ', reply_markup=adviсe_menu)
    else:
        await message.answer(response_message)

@router.message(F.text == "Материалы 📔")
async def materials_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Выводим информацию, связанную с материалами', reply_markup=platform_menu)
    else:
        await message.answer(response_message)

@router.message(F.text == "Мероприятия 🎉")
async def events_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Выводим информацию, связанную с мероприятиями', reply_markup=platform_menu)
    else:
        await message.answer(response_message)