from telebot.handler_backends import State, StatesGroup

class UserRequestState(StatesGroup):
    city = State()
    date_in = State()
    date_out = State()
    hotel_amount = State()
    foto_flag = State()
    foto_amount = State()


