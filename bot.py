from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers.register_handlers import router as registration_router  # Роутер для регистрации
from handlers.general_handlers import router as general_router  # Роутер для общих обработчиков

from handlers.access_callback import router as access_users  # Роутер для доступа к платформе
from handlers.no_access_callback import router as no_access_users  # Роутер для отказа к платформе

from handlers.hello import router as hello  # Роутер для приветствия

from database.handlers.database_create import create_all_databases


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await create_all_databases()  # Ждем завершения создания базы данных

    dp.include_router(registration_router)  # Включаем роутер регистрации
    dp.include_router(general_router)  # Включаем роутер общих обработчиков
    dp.include_router(access_users)  # Включаем роутер для доступа к платформе 
    dp.include_router(no_access_users)  # Включаем роутер для доступа отказа в доступе
    dp.include_router(hello)  # Включаем роутер для приветствия пользователей
    await dp.start_polling(bot)
