from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    payment_photo = State()