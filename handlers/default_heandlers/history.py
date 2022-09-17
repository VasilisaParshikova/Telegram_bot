from telebot.types import Message
from database.MySQL_script import DB_Worker
from loader import bot


@bot.message_handler(commands=['history'])
def bot_history(message: Message):
    bot.send_message(message.chat.id, 'Вы запросили историю ваших поисковых запросов.'
                                      'Ниже вам будут отправлена информация о ваших 5 последнх запросах.')
    texts = DB_Worker().read_from_db(message.chat.id)
    for text in texts:
        bot.send_message(message.chat.id, text)
