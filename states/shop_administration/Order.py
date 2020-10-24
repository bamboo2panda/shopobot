from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderItems(StatesGroup):
    Count = State()
    Address = State()
    Amount = State()
    Qiwi = State()
