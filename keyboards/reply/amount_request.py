from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def amount_request() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    key1 = KeyboardButton('1')
    key2 = KeyboardButton('2')
    key3 = KeyboardButton('3')
    key4 = KeyboardButton('4')
    key5 = KeyboardButton('5')
    key6 = KeyboardButton('6')
    key7 = KeyboardButton('7')
    key8 = KeyboardButton('8')
    key9 = KeyboardButton('9')
    key10 = KeyboardButton('10')
    keyboard.add(key1, key2, key3, key4, key5, key6, key7, key8, key9, key10)

    return keyboard