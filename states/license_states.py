from aiogram.fsm.state import StatesGroup, State


class LicenseStates(StatesGroup):
    fullname = State()
    direction = State()
    academic_year = State()
    date = State()
    date_month = State()
    order_number = State()
