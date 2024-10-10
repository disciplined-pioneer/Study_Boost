from aiogram import Router, F
from datetime import datetime
from keyboards.platform_keyb import platform_menu
from database.requests.user_search import check_user_registration, check_user_payment
from aiogram import types
from aiogram.fsm.context import FSMContext
from states.payment_states import PaymentStates

router = Router()

@router.message(F.photo, PaymentStates.payment_photo)  # Используем фильтр для проверки типа контента
async def receive_payment_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await message.answer("Фотография успешно получена!")
    
    # Завершаем состояние
    await state.clear()

@router.message(F.text == 'Войти в систему 🚪')
async def login_handler(message: types.Message, state: FSMContext):

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
                await message.answer(f'Добро пожаловать! Доступ к платформе открыт 😊', reply_markup=platform_menu)
            else:
                await message.answer(f'Ваша подписка не оплачена! Пожалуйста, отправьте фото с вашей подпиской: ')
                await state.set_state(PaymentStates.payment_photo)  # Устанавливаем состояние ожидания фотографии
        else:
            await message.answer('Не найдены данные о платеже. Пожалуйста, свяжитесь с поддержкой.')
    else:
        await message.answer('Вы не были зарегистрированы! Пожалуйста, зарегистрируйтесь и попробуйте снова, нажав на кнопку "Регистрация 📝"!')
        