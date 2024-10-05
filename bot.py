from aiogram import Bot, Dispatcher
from aiogram import Router
from config import TOKEN
from handlers.register_handlers import router as registration_router  # Роутер для регистрации
from handlers.general_handlers import router as general_router  # Роутер для общих обработчиков
from handlers.admin_callback import router as access_users  # Роутер для административных функций
from handlers.hello import router as hello  # Роутер для приветствия


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(registration_router)  # Включаем роутер регистрации
    dp.include_router(general_router)  # Включаем роутер общих обработчиков
    dp.include_router(access_users)  # Включаем роутер для доступа пользователям
    dp.include_router(hello)  # Включаем роутер для приветствия пользователей
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
