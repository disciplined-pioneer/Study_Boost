from aiogram.fsm.state import State, StatesGroup

class PaymentStates(StatesGroup):
    payment_photo = State()
