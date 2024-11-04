from aiogram.fsm.state import State, StatesGroup

class EventsStates(StatesGroup):
    ID_user = State()
    date_publication = State()
    place = State()
    date = State()
    time = State()
    description = State()