from aiogram.fsm.state import State, StatesGroup

class HelpSuggestionStates(StatesGroup):
    content = State()