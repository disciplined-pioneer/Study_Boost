from aiogram.fsm.state import State, StatesGroup

class AdviсeStates(StatesGroup):
    category_advice = State()
    content = State()
    ID_user = State()
    date_publication = State()