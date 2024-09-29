from aiogram import Bot, Dispatcher
from aiogram import Router
from config import TOKEN
from handlers.register_handlers import router as registration_router  # Роутер для регистрации
from handlers.general_handlers import router as general_router  # Роутер для общих обработчиков

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    # Передаем экземпляр Bot в роутеры
    registration_router.bot = bot  # Устанавливаем bot для роутера регистрации
    general_router.bot = bot  # Если необходимо, устанавливаем bot для общих обработчиков

    dp.include_router(registration_router)  # Включаем роутер регистрации
    dp.include_router(general_router)  # Включаем роутер общих обработчиков
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
