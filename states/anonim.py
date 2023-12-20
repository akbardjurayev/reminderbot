from aiogram.dispatcher.filters.state import State, StatesGroup


class QuranState(StatesGroup):
    current_page = State()
    read_page = State()
