from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    name = State()
    city_university = State()
    name_university = State()
    faculty = State()
    course = State()
    payment_photo = State()