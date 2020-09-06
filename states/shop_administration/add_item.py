from aiogram.dispatcher.filters.state import StatesGroup, State


class AddItem(StatesGroup):
    Photo = State()
    Name = State()
    Description = State()
    Price = State()

    # Может понадобится
    # Payment_method = State()
