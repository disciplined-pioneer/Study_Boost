from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    name = State()
    university_city = State()
    name_university = State()
    course = State()
    faculty = State()
    payment_photo = State()
    password = State()
