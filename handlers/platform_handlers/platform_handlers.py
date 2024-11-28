from aiogram import types
from aiogram import Router, F

from keyboards.advice_keyb import advice_menu
from keyboards.events_keyb import events_menu
from keyboards.platform_keyb import settings_menu
from keyboards.material_keyb import material_menu
from keyboards.registration_keyb import registration_menu

router = Router()

@router.message(F.text.in_(["Советы 🦉", "Материалы 📔", "Мероприятия 🎉"]))
async def general_handler(message: types.Message):
    menus = {
        "Советы 🦉": advice_menu,
        "Материалы 📔": material_menu,
        "Мероприятия 🎉": events_menu
    }
    await message.reply("Выберите одну из опций ниже:", reply_markup=menus.get(message.text))

@router.message(F.text == "Настройки ⚙️")
async def setting_handler(message: types.Message):

    await message.reply(f'Вы перешли в настройки платформы ⚙️', reply_markup=settings_menu)

@router.message(F.text == 'Меню оплаты ◀️')
async def back_menu_handler(message: types.Message):

    await message.reply(f'Вы вернулись в меню регистрации 🙂', reply_markup=registration_menu)