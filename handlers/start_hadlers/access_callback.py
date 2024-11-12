from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from keyboards.admin_keyb import subscription_menu
from keyboards.platform_keyb import platform_menu
from handlers.start_hadlers.register_handlers import new_users

from database.requests.user_search import count_referrals
from database.handlers.database_handler import add_user_rating_history
from database.handlers.database_handler import register_user, add_subscription_status, add_payment

router = Router()

@router.callback_query(F.data == "access")
async def access(callback: CallbackQuery, bot: Bot):

    # Получаем ID администратора и ID сообщения, по которому кликнули
    admin_id = callback.from_user.id
    message_id = callback.message.message_id

    # Редактируем текущее сообщение, заменяя только клавиатуру
    await bot.edit_message_reply_markup(chat_id=admin_id, message_id=message_id, reply_markup=subscription_menu)
    await callback.answer()

# Функция для получения информации о пользователе
async def get_user_info(callback: CallbackQuery, users_list):
    current_message_id = callback.message.message_id - 1
    return next((user for user in users_list if user['ID_message'] == current_message_id), None)

# Функция для расчета даты окончания подписки
def calculate_expiration_date(payment_date, subscription_type):
    days = {
        'Basic Month': 30,
        'Premium': 30,
        'Basic Two Month': 60,
        'Three Month': 90,
        'Unlimited': 36500
    }.get(subscription_type, 0)
    return payment_date + timedelta(days=days)

# Функция для уведомления пользователя о подписке
async def notify_user(bot: Bot, user_id, subscription_type, bonus_awarded: bool = False):

    text = (
        f"Вам предоставлен доступ к платформе StudyBoost с подпиской «{subscription_type}»! ✅"
        f"{'\n\nТакже вам начислено 10 баллов за регистрацию по реферальной ссылке.' if bonus_awarded else ''}"
    )
    
    await bot.send_message(user_id, text, reply_markup=platform_menu)


# Функция для уведомления реферала
async def notify_referrer(bot: Bot, referrer_id, user_id, now_date):
    
    referral_count = await count_referrals(referrer_id)
    referral_message = f"У Вас появился новый реферал! ✅ \nВаш рейтинг был повышен на +5 баллов! \nВсего рефералов на данный момент: {referral_count}"
    await add_user_rating_history(advice_id='None', material_id='None', id_user=referrer_id, granted_by=user_id, accrual_date=now_date, action_type="new_referral", rating_value='5')
    
    await bot.send_message(chat_id=referrer_id, text=referral_message)
    
    if referral_count == 10:
        
        await add_subscription_status(referrer_id, 'Unlimited')
        await add_payment(referrer_id, now_date, now_date + timedelta(days=36500))
        
        # Сообщение о статусе "Unlimited"
        await bot.send_message(
            referrer_id,
            (
                "🎉 Поздравляем! 🎉\n\n"
                "Вы успешно пригласили 10 рефералов и получили статус подписки <b>Unlimited</b>! ✅\n\n"
                "Теперь у вас <b>неограниченный доступ</b> ко всем возможностям нашей платформы.\n"
                "Откройте для себя больше возможностей и продолжайте делиться ими с друзьями! 🚀"
            ),
            reply_markup=platform_menu,
            parse_mode="HTML"
        )

# Основная функция для выбора подписки
@router.callback_query(F.data.startswith('subscription_'))
async def subscription_choice(callback: CallbackQuery, bot: Bot):

    # Получаем информацию о пользователе
    user_info = await get_user_info(callback, new_users)
    if not user_info:
        await callback.message.answer("Пользователь для данной подписки не найден.")
        return

    # Обновляем подписку и записываем в БД
    subscription_type = callback.data.replace('subscription_', '').replace('_', ' ').title()
    user_id = user_info["ID_user"]
    user_info['subscription_type'] = subscription_type
    await register_user(user_info)
    await add_subscription_status(user_id, subscription_type)

    # Расчет и запись даты окончания подписки
    payment_date = user_info['date_registration']
    expiration_date = calculate_expiration_date(payment_date, subscription_type)
    await add_payment(user_id, payment_date, expiration_date)

    # Удаляем пользователя из списка новых и отправляем уведомления
    new_users.remove(user_info)

    # Проверка и уведомление реферала
    now_date = datetime.now().date()
    referrer_id = user_info.get('referrer_id')
    if referrer_id != 'None':
        await notify_referrer(bot, referrer_id, user_id, now_date)
        await add_user_rating_history(advice_id='None', material_id='None', id_user=user_id,
                                      granted_by=referrer_id, accrual_date=now_date, action_type="new_referral", rating_value='10')
        await notify_user(bot, user_id, subscription_type, bonus_awarded=True)
    else:
        await notify_user(bot, user_id, subscription_type, bonus_awarded=True)

    # Подтверждение администратору
    await callback.message.answer(f"Вы предоставили доступ пользователю с ID: {user_id} ✅")
    await callback.message.edit_reply_markup(reply_markup=None)
