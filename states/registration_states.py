from aiogram.dispatcher import FSMContext
from aiogram.fsm.state import StatesGroup, State

class RegistrationStates(StatesGroup):
    name = State()
    university_city = State()
    name_university = State()
    course = State()
    faculty = State()