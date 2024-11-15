from aiogram.fsm.state import State, StatesGroup

class MaterialStates(StatesGroup):
    faculty = State()
    course = State()
    type_material = State()
    topic = State()
    description_material = State()
    photos_id = State()