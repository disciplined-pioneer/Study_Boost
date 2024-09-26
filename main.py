import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from registration.registration import register_handlers  # Импортируем функцию для регистрации хэндлеров

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    register_handlers(dp)  # Регистрируем обработчики
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('The bot was stopped')
