from aiogram import Bot, Dispatcher
from aiogram import Router
from config import TOKEN
from registration.registration import register_handlers  # Импортируем функцию для регистрации хэндлеров

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создайте роутер
router = Router()

async def main():
    register_handlers(router)  # Регистрируем обработчики
    dp.include_router(router)  # Включаем роутер в диспетчер
    await dp.start_polling(bot)