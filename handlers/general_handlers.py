from aiogram import Router, F
from aiogram.types import Message
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

    
@router.message(F.text == 'Оплата подписки 💵')
async def login_handler(message: Message):
    await message.answer('Здесь объясним как оплатить подписку и стоимость каждой из них')

@router.message(F.text == 'Инструкция 📕')
async def instruction_handler(message: Message):

    # Отправляем документ
    await message.bot.send_document(
        chat_id=message.from_user.id,
        document='BQACAgIAAxkBAAIQJWb-yNqpCOhKkViHeQp96c48vuHgAAKEaAAC1Tr5Sz35edJ2tLeBNgQ',
        caption = f'Инструкция содержит подробное описание всех функций платформы, пошаговое руководство по регистрации и использованию бота, а также примеры обмена учебными материалами и заработка очков за активность',
    )

@router.message(F.text == 'Создатель ©️')
async def creator_handler(message: Message):
    text = (
        "Привет, Я Virtu! 👨‍💻\n\n"
        "Я являюсь разработчиком этого Telegram-бота и Python-разработчиком, специализирующимся на Data Science 🤖\n\n"
        "Моя цель — создавать полезные и удобные инструменты, которые помогут студентам эффективно обмениваться знаниями и учебными материалами 📚\n\n"
        "Я студент первого курса, и этот бот был разработан для того, чтобы упростить жизнь студентов. Если у вас есть идеи или предложения, буду рад их услышать! 😉\n\n"
        "Для вопросов или предложений вы можете связаться со мной через почту virtu1129@gmail.com  📩"
    )

    # ID фотографии
    photo_id = 'AgACAgIAAxkBAAIIg2b6x72lvUPWCK_udjCgFdxTAAHamQAC2usxG3jT2UuwWltlE_cjTgEAAwIAA3kAAzYE'  # замените на фактический ID фотографии

    await message.answer_photo(photo=photo_id, caption=text, parse_mode='Markdown')

@router.message(F.text == 'Помощь ❓')
async def help_handler(message: Message):
    await message.answer('Просим отправить вопрос, по которому пользователь хотел обратиться')
