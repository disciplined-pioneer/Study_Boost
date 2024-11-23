import os
import json
import zipfile

from aiogram.types import FSInputFile
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboards.material_keyb import material_menu
from keyboards.cancellation_states import cancel_state

from states.material_state import View_materials
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database.requests.user_access import can_use_feature
from handlers.platform_handlers.material_handlers.search_material_handlers import get_all_materials, get_file_id_material

router = Router()

# Переменная для временного хранения найденных материалов
user_results = {}

@router.message(F.text == 'Поиск материалов 🔍')
async def send_welcome(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        text = (
            "🔎 <b>Поиск материалов</b>\n\n"
            "Введите <i>ключевое слово</i> или <i>фразу</i>, чтобы найти подходящий материал.\n\n"
            "📚 <b>Примеры:</b>\n"
            "— математика\n"
            "— программирование\n"
            "— 1 курс\n\n"
            "✨ Мы найдём все материалы, соответствующие вашему запросу!"
        )

        await message.reply(text, reply_markup=cancel_state, parse_mode="HTML")
        await state.set_state(View_materials.keyword)
        
    else:
        await message.answer(response_message)

@router.message(View_materials.keyword)
async def search_materials(message: types.Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить ❌']:

        # Запрос на поиск всех материалов
        materials = await get_all_materials()
        query = message.text.strip().lower()
        await state.update_data(keyword=query)

        if not query:
            await message.reply("Пожалуйста, введите запрос для поиска.")
            return
        
        # Поиск материалов по ключевому слову в названии и описании
        result_materials = [
            material for material in materials
            if query in material["faculty"].lower() or query in material["course"].lower() or query in material["subject"].lower() or query in material["topic"].lower() or query in material["description_material"].lower()
        ]

        if not result_materials:
            await message.reply("К сожалению, ничего не найдено по вашему запросу 😕")
            return
        
        # Сохраняем найденные материалы для пользователя
        user_results[message.chat.id] = result_materials

        # Создаем меню
        all_material = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=el['topic'], callback_data=f'material_id:{el["material_id"]}')] for el in result_materials
            ]
        )

        # Выводим результаты поиска
        response_text = "Выберите материал по названию темы:"
        await message.reply(response_text, reply_markup=all_material)
    
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)


# Обработчик материалов
@router.callback_query(lambda c: c.data.startswith("material_id"))
async def material_id(callback_query: CallbackQuery, state: FSMContext):

    # Запрос на поиск всех материалов
    materials = await get_all_materials()
    material_id = callback_query.data.split(':')[-1]
    element = next((material for material in materials if material['material_id'] == material_id), None)

    if element is None:
        await callback_query.answer("Материал не найден.")
        return

    # Клавиатура с кнопками "🔑 Скачать" и "◀️ Назад"
    download_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='🔑 Скачать', callback_data=f'download:{material_id}')],
            [InlineKeyboardButton(text='◀️ Назад', callback_data='back')]
        ]
    )

    # Выводим информацию о выбранном материале
    await callback_query.message.edit_text(
        f"🎓 <b>Факультет:</b> {element['faculty']}\n\n"
        f"📘 <b>Курс:</b> {element['course']}\n\n"
        f"📚 <b>Предмет:</b> {element['subject']}\n\n"
        f"📄 <b>Тип материала:</b> {element['type_material']}\n\n"
        f"📌 <b>Тема:</b> {element['topic']}\n\n\n"
        f"📝 <b>Описание:</b>\n{element['description_material']}\n\n"
        "⬇️ Выберите действие ниже:",
        reply_markup=download_menu,
        parse_mode="HTML"
    )
    await state.update_data(topic=element['topic'])

# Обработчик скачивания
@router.callback_query(lambda c: c.data.startswith("download:"))
async def download_material(callback_query: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    bot = callback_query.bot
    user_id = str(callback_query.from_user.id) 
    material_id = int(callback_query.data.split(':')[-1])
    
    # Получаем список файлов из БД
    files_data_text = await get_file_id_material(material_id)  # Здесь ваш метод получения данных из БД
    files_data = json.loads(files_data_text.replace("'", '"'))
    file_ids = [item['file_id'] for item in files_data]  # Извлекаем только file_id
    
    # Создаём временную папку для хранения файлов
    user_folder = f"temp_zip/{user_id}"
    os.makedirs(user_folder, exist_ok=True)
    zip_filename = f"{user_folder}/{data['topic']}.zip"

    # Загружаем файлы и создаём ZIP-архив
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for idx, file_id in enumerate(file_ids):
            file = await bot.get_file(file_id)  # Получаем файл с сервера Telegram
            local_file_path = os.path.join(user_folder, f"file_{idx}.{file.file_path.split('.')[-1]}")
            await bot.download_file(file.file_path, local_file_path)  # Загружаем файл
            
            zipf.write(local_file_path, f"file_{idx}.{file.file_path.split('.')[-1]}")  # Добавляем в архив
            os.remove(local_file_path)  # Удаляем временный файл после добавления в архив

    # Отправляем архив пользователю
    document = FSInputFile(zip_filename)
    caption_text = (
        "Ваши материалы успешно обработаны 📂\n\n"
        "Файлы сохранены в архиве. Спасибо за использование нашего сервиса!"
    )
    await callback_query.message.answer_document(document, caption=caption_text, reply_markup=material_menu)
    
    # Удаляем временные данные
    os.remove(zip_filename)
    os.rmdir(user_folder)

    await callback_query.answer()
    await state.clear()

# Обработчик кнопки "◀️ Назад"
@router.callback_query(lambda c: c.data == "back")
async def go_back(callback_query: CallbackQuery):
    user_id = callback_query.message.chat.id

    # Получаем результаты поиска для этого пользователя
    result_materials = user_results.get(user_id)

    if not result_materials:
        await callback_query.message.edit_text("Поиск был сброшен. Введите запрос заново.")
        return

    # Восстанавливаем меню материалов
    old_material_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=el['topic'], callback_data=f'material_id:{el["material_id"]}')] for el in result_materials
        ]
    )

    # Возвращаем сообщение с результатами поиска
    await callback_query.message.edit_text(
        "Выберите материал по названию темы:",
        reply_markup=old_material_menu
    )