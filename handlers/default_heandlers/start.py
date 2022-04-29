from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}! "
                          f"Я - бот по поиску отелей. Напиши /help для получения справки по командам")

