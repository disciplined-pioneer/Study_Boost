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
    text = (
        "Привет, Я Virtu! 👨‍💻\n\n"
        "Я являюсь разработчиком этого Telegram-бота и Python-разработчиком, специализирующимся на Data Science 🤖\n\n"
        "Моя цель — создавать полезные и удобные инструменты, которые помогут студентам эффективно обмениваться знаниями и учебными материалами 📚\n\n"
        "Я студент первого курса, и этот бот был разработан для того, чтобы упростить жизнь студентов. Если у вас есть идеи или предложения, буду рад их услышать! 😉\n\n"
        "Для вопросов или предложений вы можете связаться со мной через почту virtu1129@gmail.com)  📩"
    )

    # ID фотографии
    photo_id = 'AgACAgIAAxkBAAIIg2b6x72lvUPWCK_udjCgFdxTAAHamQAC2usxG3jT2UuwWltlE_cjTgEAAwIAA3kAAzYE'  # замените на фактический ID фотографии

    await message.answer_photo(photo=photo_id, caption=text, parse_mode='Markdown')

@router.message(F.text == 'Помощь ❓')
async def help_handler(message: Message):
    await message.answer('Просим отправить вопрос, по которому пользователь хотел обратиться')
