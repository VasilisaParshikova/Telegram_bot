from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def yes_no_reply() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    key_yes = KeyboardButton('Да')
    key_no = KeyboardButton('Нет')
    keyboard.add(key_yes, key_no)
    return keyboard

