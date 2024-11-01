from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда для генерации реферальной ссылки
@dp.message(Command("referral"))
async def referral_handler(message: Message):
    user_id = message.from_user.id  # Уникальный идентификатор пользователя
    referral_link = f"https://t.me/StudyBoost_bot?start={user_id}"
    
    await message.answer(
        f"Ваша реферальная ссылка:\n{referral_link}\n\n"
        "Отправьте эту ссылку своим друзьям. Если они перейдут по ней и начнут использовать бота, "
        "вы получите бонусы!"
    )

# Обработчик команды /start для обработки реферального кода
@dp.message(CommandStart())
async def start_handler(message: Message, command: CommandStart):
    ref_code = command.args  # Получаем реферальный код (user_id пригласившего)

    if ref_code:
        # Можно сохранить информацию о реферале или выдать бонусы пригласившему
        await message.answer(
            f"Добро пожаловать! Вы пришли по реферальной ссылке от пользователя с ID: {ref_code}"
        )
    else:
        await message.answer("Добро пожаловать!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
