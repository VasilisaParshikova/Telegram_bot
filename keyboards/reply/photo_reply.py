from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def photo_reply() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    key_yes = KeyboardButton('Списком')
    key_no = KeyboardButton('С фото')
    keyboard.add(key_yes, key_no)
    return keyboard

