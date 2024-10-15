from aiogram import Router, F
from aiogram import types
from keyboards.platform_keyb import platform_menu
from database.requests.user_search import check_user_registration, check_user_payment

from datetime import datetime

router = Router()

@router.message(F.text == "Советы 🦉")
async def adviсe_handler(message: types.Message):

    # Проверка наличия пользователя в БД
    user_id = message.from_user.id
    result, _ = await check_user_registration(user_id)

    if result:

        # Проверяем, действует ли ещё подписка
        user_payment = await check_user_payment(user_id)
        
        if user_payment:
            expiration_date = user_payment[3]  # Предполагается, что expiration_date находится на 4-й позиции
            now_date = datetime.now().date()
            expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()

            if expiration_date > now_date:
                await message.answer(f'Выводим информацию, связанную с советами', reply_markup=platform_menu)
            else:
                await message.answer(f'Ваша подписка не оплачена! Пожалуйста, нажмите на кнопку "Войти в систему 🚪" и предоставьте фото оплаты')
        else:
            await message.answer('Не найдены данные о платеже. Пожалуйста, свяжитесь с поддержкой.')
    else:
        await message.answer('Вы не были зарегистрированы! Пожалуйста, зарегистрируйтесь и попробуйте снова, нажав на кнопку "Регистрация 📝"!')
