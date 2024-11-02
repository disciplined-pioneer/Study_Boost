from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from keyboards.admin_keyb import subscription_menu
from keyboards.platform_keyb import platform_menu
from handlers.start_hadlers.register_handlers import new_users
from database.handlers.database_handler import register_user, add_subscription_status, add_payment
from database.requests.user_search import count_referrals

router = Router()

@router.callback_query(F.data == "access")
async def access(callback: CallbackQuery, bot: Bot):

    # Получаем ID администратора и ID сообщения, по которому кликнули
    admin_id = callback.from_user.id
    message_id = callback.message.message_id

    # Редактируем текущее сообщение, заменяя только клавиатуру
    await bot.edit_message_reply_markup(chat_id=admin_id, message_id=message_id, reply_markup=subscription_menu)
    await callback.answer()

@router.callback_query(F.data.startswith('subscription_'))
async def subscription_choice(callback: CallbackQuery, bot: Bot):

    # Получаем выбранный тип подписки из данных callback
    subscription_type = callback.data.replace('subscription_', '').replace('_', ' ').title()

    # Получаем ID текущего сообщения и ищем пользователя
    current_message_id = callback.message.message_id - 1
    user_info = next((user for user in new_users if user['ID_message'] == current_message_id), None)

    # Проверка, найден ли пользователь
    if not user_info:
        await callback.message.answer("Пользователь для данной подписки не найден.")
        return

    user_id = user_info["ID_user"]
    user_info['subscription_type'] = subscription_type

    # Обновляем данные пользователя и регистрируем пользователя в БД
    await register_user(user_info)
    await add_subscription_status(user_id, subscription_type)

    # Расчет даты окончания подписки и добавление в БД
    payment_date = user_info['date_registration']
    expiration_date = payment_date + timedelta(days={
        'Basic Month': 30,
        'Premium': 30,
        'Basic Two Month': 60,
        'Three Month': 90,
        'Unlimited': 36500
    }.get(subscription_type, 0))
    await add_payment(user_id, payment_date, expiration_date)
    new_users.remove(user_info)

    # Отправляем уведомление пользователю
    await bot.send_message(
        user_id,
        f"Вам был предоставлен доступ к платформе StudyBoost с подпиской: {subscription_type}! ✅",
        reply_markup=platform_menu
    )

    # Отправляем сообщение рефералу, если он есть
    referrer_id = user_info['referrer_id']
    if referrer_id and referrer_id != 'None':
        referral_count = await count_referrals(referrer_id)
        referral_message = f"У Вас появился новый реферал! ✅ \nВсего рефералов на данный момент: {referral_count}"

        # Изменяем статус подписки, если нужно
        if referral_count == 1:
            now_date = datetime.now().date()
            await add_subscription_status(referrer_id, 'Unlimited')
            await add_payment(referrer_id, now_date, now_date + timedelta(36500))

            # Отправляем уведомление о результате обновления подписки
            await bot.send_message(
                referrer_id,
                (
                    "🎉 Поздравляем! 🎉\n\n"
                    "Вы успешно пригласили 10 рефералов и получили статус подписки <b>Unlimited</b>! ✅\n\n"
                    "Теперь у вас <b>неограниченный доступ</b> ко всем возможностям нашей платформы.\n\n"
                    "Откройте для себя больше возможностей и продолжайте делиться ими с друзьями! 🚀"
                ),
                reply_markup=platform_menu,
                parse_mode="HTML"
            )
        
        # Отправка сообщения рефералу
        await bot.send_message(chat_id=referrer_id, text=referral_message)

    # Подтверждаем действие администратору
    await callback.message.answer(f"Вы предоставили доступ пользователю с ID: {user_id} ✅")
    await callback.message.edit_reply_markup(reply_markup=None)