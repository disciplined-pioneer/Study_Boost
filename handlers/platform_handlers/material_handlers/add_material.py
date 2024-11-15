from aiogram import types

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from states.material_state import MaterialStates

from keyboards.material_keyb import material_menu
from keyboards.cancellation_states import complete_process, cancel_state

router = Router()

# Обработчик для кнопки "Добавить материал ➕"
@router.message(F.text == 'Добавить материал ➕')
async def add_material(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали добавление материала. Пожалуйста, укажите факультет. Пример: Факультет информационных технологий.", reply_markup=cancel_state)
    await state.set_state(MaterialStates.faculty)

# Обработчик для ввода факультета
@router.message(MaterialStates.faculty)
async def process_faculty(message: types.Message, state: FSMContext):
    if message.text != '/cancellation' and message.text != 'Отменить состояние':
        faculty = message.text
        await state.update_data(faculty=faculty)
        await message.answer("Теперь укажите курс. Пример: 1 курс.")
        await state.set_state(MaterialStates.course)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)

# Обработчик для ввода курса
@router.message(MaterialStates.course)
async def process_course(message: types.Message, state: FSMContext):
    if message.text != '/cancellation' and message.text != 'Отменить состояние':
        course = message.text
        await state.update_data(course=course)
        await message.answer("Теперь укажите тип материала. Пример: Лекция, Конспект.")
        await state.set_state(MaterialStates.type_material)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)

# Обработчик для ввода типа материала
@router.message(MaterialStates.type_material)
async def process_type_material(message: types.Message, state: FSMContext):
    if message.text != '/cancellation' and message.text != 'Отменить состояние':
        type_material = message.text
        await state.update_data(type_material=type_material)
        await message.answer("Теперь укажите тему материала. Пример: Операционные системы.")
        await state.set_state(MaterialStates.topic)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)

# Обработчик для ввода темы
@router.message(MaterialStates.topic)
async def process_topic(message: types.Message, state: FSMContext):
    if message.text != '/cancellation' and message.text != 'Отменить состояние':
        topic = message.text
        await state.update_data(topic=topic)
        await message.answer("Теперь опишите материал. Пример: В этой лекции рассматриваются основные понятия операционных систем.")
        await state.set_state(MaterialStates.description_material)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)

# Обработчик для ввода описания материала
@router.message(MaterialStates.description_material)
async def process_description_material(message: types.Message, state: FSMContext):
    if message.text != '/cancellation' and message.text != 'Отменить состояние':
        description_material = message.text
        await state.update_data(description_material=description_material)
        await message.answer("Теперь отправьте фотографию материала. Пример: сканированная лекция или конспект.")
        await state.set_state(MaterialStates.files_id)
    else:
        await state.clear()
        await message.answer('Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊', reply_markup=material_menu)


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
    await message.answer(
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
    await message.answer(
        "Документ успешно добавлен! Вы можете отправить ещё документы, фотографии или завершить процесс.",
        reply_markup=complete_process
    )

# Обработчик для завершения процесса (теперь обычная асинхронная функция)
async def finish_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    files = data.get('files', [])  # Получаем общий список файлов
    if files:
        response = "Процесс завершён. Вот ваши данные:\n"
        for file in files:
            response += f"Тип: {file['type']}, ID: {file['file_id']}\n\n"  # Выводим тип и ID каждого файла
        await message.answer(response, disable_web_page_preview=True)
    else:
        await message.answer("Вы не отправили ни фотографий, ни документов.")

    # Сброс состояния после завершения процесса
    await state.clear()


# Обработчик для различных действий (завершение или отмена состояния)
@router.message(F.text, MaterialStates.files_id)
async def cancel_material(message: types.Message, state: FSMContext):

    # Завершение
    if message.text == "Завершить ❌":
        await finish_process(message, state)  # Вызываем функцию завершения процесса
        return

    # Проверка на отмену состояния
    if message.text in ['/cancellation', 'Отменить состояние']:
        await state.clear()  # Очищаем состояние
        await message.answer(
            'Вы вышли из текущего режима и вернулись в основной режим работы с ботом 😊',
            reply_markup=material_menu
        )
        return
