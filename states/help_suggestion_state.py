from aiogram.fsm.state import State, StatesGroup

class HelpStates(StatesGroup):
    content = State()

class SuggestionsStates(StatesGroup):
    content = State()