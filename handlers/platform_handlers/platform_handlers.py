from aiogram import types
from aiogram import Router, F

from keyboards.advice_keyb import advice_menu
from keyboards.events_keyb import events_menu
from keyboards.platform_keyb import settings_menu
from keyboards.material_keyb import material_menu

from database.requests.user_access import can_use_feature

router = Router()

@router.message(F.text == "Советы 🦉")
async def adviсe_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply(f'Выберите одну из опций ниже: ', reply_markup=advice_menu)
    else:
        await message.reply(response_message)

@router.message(F.text == "Материалы 📔")
async def materials_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply(f'Выберите одну из опций ниже: ', reply_markup=material_menu)
    else:
        await message.reply(response_message)

@router.message(F.text == "Мероприятия 🎉")
async def events_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply("Выберите одну из опций ниже:", reply_markup=events_menu)
    else:
        await message.reply(response_message)

@router.message(F.text == "Настройки ⚙️")
async def events_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.reply(f'Вы перешли в настройки платформы ⚙️', reply_markup=settings_menu)
    else:
        await message.reply(response_message)