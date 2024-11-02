from aiogram import types
from aiogram import Router, F
from aiogram.types import Message

from keyboards.platform_keyb import platform_menu
from database.requests.user_access import can_use_feature

router = Router()

@router.message(F.text == 'Команды 📜')
async def commands_handler(message: Message):
    commands_text = (
        "<b>Доступные команды:</b>\n\n"
        "<b>/start</b> - Начало работы с ботом, активация и первоначальные настройки.\n\n"
        "<b>/my_data</b> - Просмотр информации о вашем аккаунте, включая историю активности и личные данные.\n\n"
        "<b>/my_rating</b> - Отображение текущего рейтинга и прогресса.\n\n"
        "<b>/referal_link</b> - Ваша уникальная реферальная ссылка для приглашения друзей.\n\n"
        "<b>/my_referal</b> - Просмотр количества приглашённых вами друзей и описание ваших бонусов.\n\n"
        "<b>/top_users</b> - Список Топ-10 пользователей с наивысшим рейтингом."
    )
    await message.answer(commands_text, parse_mode="HTML")

@router.message(F.text == "Назад 🔙")
async def back_handler(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(f'Вы вернулись в главное меню 😊', reply_markup=platform_menu)
    else:
        await message.answer(response_message)