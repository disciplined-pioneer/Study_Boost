from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Дать доступ")
async def grant_access(message: Message):
    # Логика для дачи доступа пользователю
    await message.answer("Доступ предоставлен!")

@router.message(F.text == "Не дать доступ")
async def deny_access(message: Message):
    # Логика для отказа в доступе пользователю
    await message.answer("Доступ не предоставлен.")
