import time
from datetime import datetime

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from states.material_state import MaterialStates

from database.requests.user_access import can_use_feature
from NI_assistants.sentiment_text import analyze_sentiment
from database.handlers.database_handler import add_material

from keyboards.material_keyb import material_menu, type_material
from keyboards.cancellation_states import complete_process, cancel_state

router = Router()

# Обработчик для кнопки "Добавить материал ➕"
@router.message(F.text == 'Добавить материал ➕')
async def process_add_material(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:
        await message.answer(
        "❌ Чтобы завершить процесс добавления материала, нажмите кнопку *«Отменить состояние»*. \n\n",
        reply_markup=cancel_state,
        parse_mode="Markdown")
        time.sleep(3)
        
        await message.answer("Вы выбрали добавление материала. Пожалуйста, укажите факультет. Пример: Информатика и вычислительная техника.", reply_markup=cancel_state)
        await state.set_state(MaterialStates.faculty)
    else:
        await message.answer(response_message)

# Обработчик для ввода факультета
@router.message(MaterialStates.faculty)
async def process_faculty(message: types.Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить состояние ❌']:
        
        # Проверка качества текста
        faculty = message.text
        sentiment_score = await analyze_sentiment(faculty)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            return
        
        await state.update_data(faculty=faculty)
        await message.reply("Теперь укажите курс. Пример: 1 курс.")
        await state.set_state(MaterialStates.course)
    else:
        await state.clear()
        await message.reply('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)

# Обработчик для ввода курса
@router.message(MaterialStates.course)
async def process_course(message: types.Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить состояние ❌']:

        # Проверка качества текста
        course = message.text
        sentiment_score = await analyze_sentiment(course)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            return
        
        await state.update_data(course=course)
        await message.reply("Теперь укажите название предмета. Пример: Операционные системы.")
        await state.set_state(MaterialStates.subject)
    else:
        await state.clear()
        await message.reply(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=material_menu
        )

# Обработчик для ввода названия предмета
@router.message(MaterialStates.subject)
async def process_subject(message: types.Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить состояние ❌']:

        # Проверка качества текста
        subject = message.text
        sentiment_score = await analyze_sentiment(subject)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            return
        
        await state.update_data(subject=subject)
        await message.reply("Теперь укажите тип материала, нажав на одну из кнопок ниже", reply_markup=type_material)
        await state.set_state(MaterialStates.type_material)
    else:
        await state.clear()
        await message.reply(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=material_menu
        )

@router.message(MaterialStates.type_material)
async def process_type_material(message: types.Message, state: FSMContext):
    if message.text not in ['/cancellation', 'Отменить состояние ❌']:
        # Преобразуем текст в код материала
        material_mapping = {
            'Лекция 📚': 'lecture',
            'Домашняя работа 🏠': 'homework',
            'Контрольная работа 📝': 'test',
            'Лабораторная работа 🔬': 'laboratory_work'
        }
        material_code = material_mapping.get(message.text)
        
        if not material_code:
            await message.reply("Неверный выбор. Пожалуйста, выберите тип материала, используя кнопки ниже.")
            return

        # Проверка качества текста
        sentiment_score = await analyze_sentiment(material_code)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            return

        await state.update_data(type_material=material_code)
        await message.reply(
            "Теперь укажите тему материала. Пример: Основы программирования.",
            reply_markup=cancel_state
        )
        await state.set_state(MaterialStates.topic)
    else:
        await state.clear()
        await message.reply(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=material_menu
        )


# Обработчик для ввода темы
@router.message(MaterialStates.topic)
async def process_topic(message: types.Message, state: FSMContext):

    if message.text not in ['/cancellation', 'Отменить состояние ❌']:

        # Проверка качества текста
        topic = message.text
        sentiment_score = await analyze_sentiment(topic)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            return
        
        await state.update_data(topic=topic)
        await message.reply("Теперь опишите материал. Пример: В этой лекции рассматриваются основные понятия операционных систем.")
        await state.set_state(MaterialStates.description_material)
    else:
        await state.clear()
        await message.reply(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=material_menu
        )

# Обработчик для ввода описания материала
@router.message(MaterialStates.description_material)
async def process_description_material(message: types.Message, state: FSMContext):
    if message.text not in ['/cancellation', 'Отменить состояние ❌']:
        
        # Проверка качества текста
        description_material = message.text
        sentiment_score = await analyze_sentiment(description_material)
        if sentiment_score <= -0.01:
            await message.reply("Ваш текст содержит негативные выражения. Пожалуйста, попробуйте переформулировать свой текст")
            return
        
        await state.update_data(description_material=description_material)
        await message.reply("Теперь отправьте фотографию материала или документ. Пример: сканированная лекция, конспект или word документ и т.д.")
        await state.set_state(MaterialStates.files_id)
    else:
        await state.clear()
        await message.reply('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)


# Обработчик для получения фотографий и добавления их в общее хранилище
@router.message(MaterialStates.files_id, F.content_type == 'photo')
async def process_photo(message: types.Message, state: FSMContext):

    # Получаем список фотографий
    photos_info = message.photo
    photos_id = [photo.file_id for photo in photos_info]  # Сохраняем все фотографии

    # Получаем данные состояния
    data = await state.get_data()
    files = data.get('files', [])  # Получаем общий список данных
    files.append({'type': 'photo', 'file_id': photos_id[-1]})  # Добавляем фотографию с указанием типа

    # Обновляем данные состояния
    await state.update_data(files=files)
    await message.reply(
        "Фотография успешно добавлена! Вы можете отправить ещё фотографии, документы или завершить процесс.",
        reply_markup=complete_process
    )

# Обработчик для получения документов и добавления их в общее хранилище
@router.message(MaterialStates.files_id, F.content_type == 'document')
async def process_document(message: types.Message, state: FSMContext):

    # Получаем документ
    document = message.document
    document_id = document.file_id  # Сохраняем file_id документа

    # Получаем данные состояния
    data = await state.get_data()
    files = data.get('files', [])  # Получаем общий список данных
    files.append({'type': 'document', 'file_id': document_id})  # Добавляем документ с указанием типа

    # Обновляем данные состояния
    await state.update_data(files=files)
    await message.reply(
        "Документ успешно добавлен! Вы можете отправить ещё документы, фотографии или завершить процесс.",
        reply_markup=complete_process
    )

# Обработчик для завершения процесса (теперь обычная асинхронная функция)
async def finish_process(message: types.Message, state: FSMContext):
    data = await state.get_data()

    # Добавление данных в БД
    await add_material(
        ID_user=str(message.from_user.id),
        date_publication=datetime.now().date(),
        faculty=data.get('faculty'),
        subject=data.get('subject'),
        course=data.get('course'),
        type_material=data.get('type_material'),
        topic=data.get('topic'),
        description_material=data.get('description_material'),
        files_id=str(data.get('files'))
    )

    files = data.get('files', [])  # Получаем общий список файлов
    if files:
        await message.reply(
                "✅ <b>Материал успешно добавлен!</b>\n\n",
                parse_mode="HTML",
                reply_markup=material_menu
            )
    else:
        await message.reply("Вы не отправили ни фотографий, ни документов.")

    # Сброс состояния после завершения процесса
    await state.clear()


# Обработчик для различных действий (завершение или отмена состояния)
@router.message(F.text, MaterialStates.files_id)
async def cancel_material(message: types.Message, state: FSMContext):

    # Завершение
    if message.text == "Завершить ✅":
        await finish_process(message, state)  # Вызываем функцию завершения процесса
        return

    # Проверка на отмену состояния
    if message.text in ['/cancellation', 'Отменить состояние ❌']:
        await state.clear()  # Очищаем состояние
        await message.reply(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=material_menu
        )
        return
