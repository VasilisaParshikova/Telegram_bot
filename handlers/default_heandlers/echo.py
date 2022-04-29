from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    bot.reply_to(message, "Вы отправили сообщение:"
                          f"{message.text}. \nЯ не могу разобрать данную команду."
                          f"Воспользуйтесь функцией /help.")
