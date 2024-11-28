import time

from config import ADMIN_ID
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.admin_keyb import access_keyboard
from keyboards.cancellation_states import cancel_state
from keyboards.registration_keyb import registration_menu

from states.registration_state import RegistrationStates

from database.requests.user_search import count_users
from database.requests.user_access import can_use_feature
from handlers.commands_handlers.commands_handlers import user_subscription

# Хранение данных новых пользователей
new_users = []
router = Router()

# Обработчик для начала регистрации
@router.message(F.text == 'Оплатить подписку 💳')
async def registration_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use == 2:
        await message.reply(response_message, reply_markup=registration_menu)

    if can_use == 1:
        await message.reply(response_message, reply_markup=registration_menu)
        await start_registration(message, state)

    if can_use == 0:
        await message.answer(
            "Чтобы отменить действие, нажмите кнопку *Отменить ❌»*. \n\n⚠️ Обратите внимание: при отмене ваш реферальный ID будет утерян. Для повторной регистрации потребуется перейти по реферальной ссылке снова.",
            parse_mode="Markdown"
        )
        await start_registration(message, state)

# Обработка фотографии
async def start_registration(message: Message, state: FSMContext):

    time.sleep(1)
    await message.answer("Пожалуйста, отправьте фото, подтверждающее оплату: ", reply_markup=cancel_state)
    await state.set_state(RegistrationStates.payment_photo)

@router.message(F.text, RegistrationStates.payment_photo)
async def cancel_registration(message: Message, state: FSMContext):
    
    # Проверка на отмену состояния
    if message.text in ['/cancellation', 'Отменить ❌']:
        await state.clear()  # Очищаем состояние
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=registration_menu)
        return

# Завершение оплаты и добавление пользователя в список
@router.message(F.photo, RegistrationStates.payment_photo)
async def finish_registration(message: Message, state: FSMContext):

    global new_users
    data = await state.get_data()
    user_id = message.from_user.id
    referrer_id = data.get("referrer_id")

    # Получаем фотографию оплаты
    payment_photo = message.photo[-1].file_id
    type_ubscription = await user_subscription(user_id)

    # Сохраняем данные пользователя
    user_info = {
        "telegram": f"@{message.from_user.username}" if message.from_user.username else "Не указан",
        "ID_user": user_id,
        "ID_message": message.message_id,
        "photo_payment": payment_photo,
        "referrer_id": referrer_id,
        "date_registration": datetime.now().date() - timedelta(days=100)
    }

    # Формируем текст для отправки админу
    user_info_text = (
        f"Телеграм: {'@' + message.from_user.username if message.from_user.username else 'Не указан'}\n\n"
        f"ID пользователя: {user_id}\n\n"
        f"ID реферера: {referrer_id or 'None'}\n\n"
        f"Количество пользователей: {await count_users()}\n\n"
        f"Тип подписки: {type_ubscription[0] if type_ubscription is not None else None}"
    )

    # Отправляем информацию админу
    await message.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=payment_photo,
        caption=user_info_text,
        reply_markup=access_keyboard
    )

    # Отправляем сообщение пользователю
    new_users.append(user_info)
    await message.answer(
        'Данные успешно были сохранены! 🎉\n\n'
        'В ближайшее время администратор проверит ваши данные и активирует подписку.\n\n'
        'После этого вы получите уведомление. Желаем вам отличного дня!', reply_markup=registration_menu
    )
    await state.clear()