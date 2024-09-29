from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == 'Войти в систему 🚪')
async def login_handler(message: Message):
    await message.answer('Запрашиваем данные на вход')

@router.message(F.text == 'Инструкция 📕')
async def instruction_handler(message: Message):
    await message.answer('Здесь нужно отправить файл pdf')

@router.message(F.text == 'Создатель ©️')
async def creator_handler(message: Message):
    await message.answer('Здесь отправляем мою фотографию и краткую информацию обо мне')

@router.message(F.text == 'Помощь ❓')
async def help_handler(message: Message):
    await message.answer('Просим отправить вопрос, по которому пользователь хотел обратиться')
