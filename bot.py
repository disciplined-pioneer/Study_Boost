from config import TOKEN
from aiogram import Bot, Dispatcher

from handlers.start_hadlers.hello import router as hello_router  # Роутер для приветствия
from handlers.start_hadlers.sign_in import router as sign_in_router # Роутер для входа в систему
from handlers.start_hadlers.register_handlers import router as registration_router  # Роутер для регистрации
from handlers.start_hadlers.general_handlers import router as general_router  # Роутер для общих обработчиков

from handlers.start_hadlers.access_callback import router as access_users_router  # Роутер для доступа к платформе
from handlers.start_hadlers.deny_access_callback import router as deny_access_users_router  # Роутер для отказа к платформе

from handlers.platform_handlers.platform_handlers import router as platform_router # Роутер для главный кнопок
from handlers.platform_handlers.setting_handlers import router as setting_router # Роутер для панели настроек

from handlers.platform_handlers.adviсe_handlers.add_adviсe import router as add_adviсe_router  # Роутер для добавления советов
from handlers.platform_handlers.adviсe_handlers.view_advice import router as view_advice_router  # Роутер для просмотра советов

from handlers.platform_handlers.material_handlers.add_material import router as add_material_router  # Роутер для добавления материалов
#from handlers.platform_handlers.material_handlers.view_material import router as view_material_router  # Роутер для просмотра материалов

from handlers.platform_handlers.events_handlers.add_events import router as add_events_router  # Роутер для добавления мероприятий
from handlers.platform_handlers.events_handlers.view_events import router as view_events_router  # Роутер для просмотра мероприятий

from commands.commands_users import router as users_router # Роутер для команд пользователей
from commands.commands_admin import router as admin_router # Роутер для команд админа

from database.handlers.database_create import create_all_databases

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await create_all_databases()  # Ждем завершения создания базы данных

    dp.include_router(hello_router)  # Включаем роутер для приветствия пользователей
    dp.include_router(sign_in_router)  # Включаем роутер для входа в систему
    dp.include_router(registration_router)  # Включаем роутер регистрации
    dp.include_router(general_router)  # Включаем роутер общих обработчиков

    dp.include_router(access_users_router)  # Включаем роутер для доступа к платформе 
    dp.include_router(deny_access_users_router)  # Включаем роутер для отказа в доступе

    dp.include_router(platform_router)  # Включаем роутер для главный кнопок
    dp.include_router(setting_router)  # Включаем роутер для кнопок настройки

    dp.include_router(add_adviсe_router)  # Включаем роутер для добавления советов
    dp.include_router(view_advice_router) # Включаем роутер для просмотра советов

    dp.include_router(add_events_router)  # Включаем роутер для добавления советов
    dp.include_router(view_events_router)  # Включаем роутер для просмотра советов

    dp.include_router(add_material_router)  # Включаем роутер для добавления материалов
    #dp.include_router(view_material_router)  # Включаем роутер для просмотра материалов

    dp.include_router(users_router) # Включаем роутер для команд пользователей
    dp.include_router(admin_router) # Включаем роутер для команд админа

    await dp.start_polling(bot)