from aiogram.fsm.state import StatesGroup, State

class add(StatesGroup):
    buildings = State()
    name = State()
    AboutMe = State()
    photos = State()
    Okk = State()

class reg(StatesGroup):
    gender = State()
    YNN = State()
class View(StatesGroup):
    view = State()