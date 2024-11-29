from datetime import datetime
from database.requests.user_search import check_user_payment

async def can_use_feature(user_id):
    user_payment = await check_user_payment(user_id)
    if not user_payment:
        text = 'Эта функция недоступна. Для доступа оформите подписку по кнопке "Оплатить подписку 💳"'
        return 0, text

    expiration_date = datetime.strptime(user_payment['expiration_date'], '%Y-%m-%d').date()
    if expiration_date <= datetime.now().date():
        text = 'Срок вашей подписки вышел! ❌\nВам доступен ограниченный функционал. Для доступа оформите подписку по кнопке  "Оплатить подписку 💳"'
        return 1, text
    else:
        text = 'Кажется, ваша подписка уже активна! Вы можете воспользоваться ботом, нажав кнопку "Войти в систему 🚪"'
        return 2, text

    