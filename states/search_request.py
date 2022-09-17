from telebot.handler_backends import State, StatesGroup

class UserRequestState(StatesGroup):
    city = State()
    date_in = State()
    date_out = State()
    distance_from_center = State()
    price_per_night_max = State()
    hotel_amount = State()
    photo_flag = State()
    database_work = State()



