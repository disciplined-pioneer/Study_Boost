from aiogram import types

from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from states.material_state import MaterialStates
from keyboards.cancellation_states import complete_process, cancel_state

router = Router()

# Создаём клавиатуру для выбора действия
async def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    add_material_button = KeyboardButton("Добавить материал ➕")
    keyboard.add(add_material_button)
    return keyboard

# Обработчик для кнопки "Добавить материал ➕"
@router.message(F.text == 'Добавить материал ➕')
async def add_material(message: types.Message, state: FSMContext):
    await message.answer("Вы выбрали добавление материала. Пожалуйста, укажите факультет. Пример: Факультет информационных технологий.", reply_markup=cancel_state)
    await state.set_state(MaterialStates.faculty)

# Обработчик для ввода факультета
@router.message(MaterialStates.faculty)
async def process_faculty(message: types.Message, state: FSMContext):
    faculty = message.text
    await state.update_data(faculty=faculty)
    await message.answer("Теперь укажите курс. Пример: 1 курс.")
    await state.set_state(MaterialStates.course)

# Обработчик для ввода курса
@router.message(MaterialStates.course)
async def process_course(message: types.Message, state: FSMContext):
    course = message.text
    await state.update_data(course=course)
    await message.answer("Теперь укажите тип материала. Пример: Лекция, Конспект.")
    await state.set_state(MaterialStates.type_material)

# Обработчик для ввода типа материала
@router.message(MaterialStates.type_material)
async def process_type_material(message: types.Message, state: FSMContext):
    type_material = message.text
    await state.update_data(type_material=type_material)
    await message.answer("Теперь укажите тему материала. Пример: Операционные системы.")
    await state.set_state(MaterialStates.topic)

# Обработчик для ввода темы
@router.message(MaterialStates.topic)
async def process_topic(message: types.Message, state: FSMContext):
    topic = message.text
    await state.update_data(topic=topic)
    await message.answer("Теперь опишите материал. Пример: В этой лекции рассматриваются основные понятия операционных систем.")
    await state.set_state(MaterialStates.description_material)

# Обработчик для ввода описания материала
@router.message(MaterialStates.description_material)
async def process_description_material(message: types.Message, state: FSMContext):
    description_material = message.text
    await state.update_data(description_material=description_material)
    await message.answer("Теперь отправьте фотографию материала. Пример: сканированная лекция или конспект.")
    await state.set_state(MaterialStates.photos_id)

# Обработчик для получения нескольких фотографий
@router.message(MaterialStates.photos_id, F.content_type == 'photo')
async def process_photo(message: types.Message, state: FSMContext):

    # Получаем список фотографий
    photos_info = message.photo
    photos_id = [photo.file_id for photo in photos_info]  # Сохраняем все фотографии
    
    # Получаем данные состояния
    data = await state.get_data()
    photos = data.get('photos', [])  # Получаем список уже добавленных фотографий
    photos.append(photos_id[-1])  # Добавляем новые фотографии в список

    # Обновляем данные состояния
    await state.update_data(photos=photos)

    # Отправляем сообщение с подтверждением и предлагаем отправить еще фотографии или завершить
    await message.answer(
        "Фотографии успешно добавлены! Вы можете отправить ещё фотографии или завершить процесс.", reply_markup=complete_process)

# Обработчик для завершения процесса
@router.message(F.text == "Завершить ❌")
async def finish_process(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    data = await state.get_data()
    photo_id = data.get('photos', [])
    print(photo_id)
    
    # Если фотографии есть, выводим их
    if photo_id:
        await message.answer(f"Процесс завершён. Вот ваши данные:\n"
                             f"Фотографии (ID):\n{photo_id}",  # Покажем все ID фотографий
                             disable_web_page_preview=True)
    else:
        await message.answer("Вы не отправили фотографий.")
    
    # Сброс состояния после завершения процесса
    await state.clear()
