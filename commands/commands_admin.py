import os

from config import ADMIN_ID

from aiogram import Router, types
from aiogram.types import FSInputFile

from database.requests.user_search import count_users

from handlers.commands_handlers.commands_handlers import recent_events

router = Router()

# Вывод всей БД
@router.message(lambda message: message.text == '/admin_commands')
async def send_db_files(message: types.Message):

    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        commands_text = (
        "<b>Доступные команды для админа:</b>\n\n"
        "<b>/admin_commands</b> - Вывод всех возможных команд.\n\n"
        "<b>/send_files</b> - Выгрузка всей база данных.\n\n"
        "<b>/count_users</b> - Количество всех пользователей в базе данных\n\n"
        "<b>/suggestions_users</b> - Вывод предложений от пользователей\n\n"
        "<b>/help_users</b> - Вывод от запросов помощи от пользователей\n\n"
        
        )
        await message.answer(commands_text, parse_mode="HTML")

    else:
        await message.answer("Доступ запрещён ❌\nЧтобы использовать эту команду, Вам необходимо обладать правами админа")

# Вывод всей база данных
@router.message(lambda message: message.text == '/send_files')
async def send_db_files(message: types.Message):

    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
    
        # Получаем все файлы с расширением .db в указанной папке
        DB_FOLDER_PATH = "database/data"
        db_files = [f for f in os.listdir(DB_FOLDER_PATH) if f.endswith(".db")]

        if not db_files:
            await message.answer("В папке нет файлов с расширением .db")
            return

        # Отправляем каждый файл
        for db_file in db_files:
            file_path = os.path.join(DB_FOLDER_PATH, db_file)

            # Создаем FSInputFile для каждого файла
            document = FSInputFile(file_path)
            await message.answer_document(document)
    else:
        await message.answer("Доступ запрещён ❌\nЧтобы использовать эту команду, Вам необходимо обладать правами админа")

# Вывод количества пользователей
@router.message(lambda message: message.text == '/count_users')
async def print_count_users(message: types.Message):

    user_id = str(message.from_user.id)
    if user_id == ADMIN_ID:
        result = await count_users()
        await message.answer(f"Количество пользователей на данный момент составляет: {result}")
    else:
        await message.answer("Доступ запрещён ❌\nЧтобы использовать эту команду, Вам необходимо обладать правами админа")

# Вывод информации о "Помощь" и "Предложения" за последние 3 дня
@router.message(lambda message: message.text == '/help_users')
async def help_events(message: types.Message):
    result = await recent_events('help')
    await message.answer(result, parse_mode="HTML")

@router.message(lambda message: message.text == '/suggestions_users')
async def suggestions_events(message: types.Message):
    result = await recent_events('suggestions')
    await message.answer(result, parse_mode="HTML")