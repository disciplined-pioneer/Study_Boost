from aiogram import Router
from aiogram import types, F
from keyboards.events_keyb import events_menu

from database.requests.events import get_events_by_period
from database.requests.user_access import can_use_feature

router = Router()

@router.message(F.text.in_(['📅 В ближайшую неделю', '🗓️ В ближайшие 2 недели', '📆 В ближайший месяц', '📅 В ближайшие 2 месяца']))
async def handle_period_buttons(message: types.Message):

    user_id = message.from_user.id
    can_use, response_message = await can_use_feature(user_id)

    if can_use:

        # Определяем период на основе текста кнопки
        period_map = {
            '📅 В ближайшую неделю': 'неделя',
            '🗓️ В ближайшие 2 недели': '2 недели',
            '📆 В ближайший месяц': 'месяц',
            '📅 В ближайшие 2 месяца': '2 месяца'
        }
        
        period = period_map[message.text]
        events_text = await get_events_by_period(period)
        
        await message.answer(events_text, reply_markup=events_menu, parse_mode="HTML")
    
    else:
        await message.answer(response_message)

