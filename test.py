from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import CallbackQuery
import asyncio

# Инициализация бота
API_TOKEN = '7512046220:AAEEv-F0mWIjMvFDQnVOST9kBWd4DYSNud0'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Симуляция данных из БД
CATEGORIES = {
    "SMM": ["Курс 1", "Курс 2", "Курс 3", "Курс 4", "Курс 5", "Курс 6"],
    "SEO": ["Курс A", "Курс B", "Курс C", "Курс D", "Курс E", "Курс F"],
    "Программирование": ["Курс X", "Курс Y", "Курс Z", "Курс W", "Курс Q", "Курс V"],
}

PAGE_SIZE = 5  # Количество курсов на странице


# Генерация кнопок для категорий
def generate_category_buttons():
    keyboard = [
        [InlineKeyboardButton(text=category, callback_data=f"category:{category}")]
        for category in CATEGORIES
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Генерация кнопок для курсов и пагинации
def generate_course_buttons(category, page, total_pages):
    keyboard = []

    # Добавляем кнопки для курсов на текущей странице
    courses = get_page_content(category, page)
    for course in courses:
        keyboard.append([InlineKeyboardButton(text=course, callback_data=f"course:{course}")])

    # Добавляем кнопки пагинации
    pagination = []
    if page > 1:
        pagination.append(InlineKeyboardButton(text="<< Назад", callback_data=f"page:{category}:{page-1}"))
    pagination.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        pagination.append(InlineKeyboardButton(text="Вперед >>", callback_data=f"page:{category}:{page+1}"))

    if pagination:
        keyboard.append(pagination)

    # Добавляем кнопку возврата к категориям
    keyboard.append([InlineKeyboardButton(text="🔙 К категориям", callback_data="categories")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Генерация контента для страницы
def get_page_content(category, page):
    items = CATEGORIES[category]
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    return items[start:end]


# Стартовое сообщение
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Добро пожаловать! Выберите интересующую вас категорию:",
        reply_markup=generate_category_buttons()
    )


# Обработчик выбора категории
@dp.callback_query(lambda c: c.data and c.data.startswith("category:"))
async def process_category(callback_query: CallbackQuery):
    category = callback_query.data.split(":")[1]
    total_pages = (len(CATEGORIES[category]) + PAGE_SIZE - 1) // PAGE_SIZE
    page = 1

    await callback_query.message.edit_text(
        f"Категория: {category}\n\nВыберите курс:",
        reply_markup=generate_course_buttons(category, page, total_pages)
    )


# Обработчик пагинации
@dp.callback_query(lambda c: c.data and c.data.startswith("page:"))
async def process_pagination(callback_query: CallbackQuery):
    _, category, page = callback_query.data.split(":")
    page = int(page)
    total_pages = (len(CATEGORIES[category]) + PAGE_SIZE - 1) // PAGE_SIZE

    await callback_query.message.edit_text(
        f"Категория: {category}\n\nВыберите курс:",
        reply_markup=generate_course_buttons(category, page, total_pages)
    )


# Обработчик выбора курса
@dp.callback_query(lambda c: c.data and c.data.startswith("course:"))
async def process_course(callback_query: CallbackQuery):
    course = callback_query.data.split(":")[1]
    await callback_query.message.edit_text(
        f"Вы выбрали курс: {course}\n\n🔙 Выберите действие:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 К категориям", callback_data="categories")],
                [InlineKeyboardButton(text="↩️ Назад к курсам", callback_data="last_category")]
            ]
        )
    )


# Обработчик возврата к категориям
@dp.callback_query(lambda c: c.data == "categories")
async def back_to_categories(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "Выберите интересующую вас категорию:",
        reply_markup=generate_category_buttons()
    )


# Обработчик возврата к последней категории
@dp.callback_query(lambda c: c.data == "last_category")
async def back_to_last_category(callback_query: CallbackQuery):
    # Здесь мы должны получить текущую категорию и страницу из вашего состояния или данных
    # Пока что можно вернуть пользователя на первую страницу первой категории
    category = "SMM"  # Этот параметр можно динамически извлекать из хранилища состояния
    page = 1
    total_pages = (len(CATEGORIES[category]) + PAGE_SIZE - 1) // PAGE_SIZE

    await callback_query.message.edit_text(
        f"Категория: {category}\n\nВыберите курс:",
        reply_markup=generate_course_buttons(category, page, total_pages)
    )


# Заглушка для "неактивной" кнопки
@dp.callback_query(lambda c: c.data == "noop")
async def noop(callback_query: CallbackQuery):
    await callback_query.answer(cache_time=30)  # Ничего не делаем


# Основная функция запуска бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
