from datetime import datetime
from database.requests.user_search import check_user_registration, check_user_payment

async def can_use_feature(user_id):

    """Проверка регистрации пользователя и статуса подписки."""
    result, _ = await check_user_registration(user_id)

    if not result:
        return False, 'Вы не были зарегистрированы! Пожалуйста, зарегистрируйтесь и попробуйте снова, нажав на кнопку "Регистрация 📝"!'

    user_payment = await check_user_payment(user_id)

    if not user_payment:
        return False, 'Не найдены данные о платеже. Пожалуйста, свяжитесь с поддержкой.'

    expiration_date = user_payment[3]  # Предполагается, что expiration_date находится на 4-й позиции
    now_date = datetime.now().date()
    expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date()

    if expiration_date <= now_date:
        return False, 'Ваша подписка не оплачена! Пожалуйста, нажмите на кнопку "Войти в систему 🚪" и предоставьте фото оплаты.'

    return True, ''