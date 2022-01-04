from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text('start command received')


def help(update, context):
    update.message.reply_text("Список команд:\n"
                              "/help — помощь по командам бота,\n"
                              "/lowprice — вывод самых дешёвых отелей в городе,\n"
                              "/highprice — вывод самых дорогих отелей в городе,\n"
                              "/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра.\n"
                              "/history — вывод истории поиска отелей\n")


def lowprice(update, context):
    update.message.reply_text('тут позже что-то будет')


def highprice(update, context):
    update.message.reply_text('тут позже что-то будет')


def bestdeal(update, context):
    update.message.reply_text('тут позже что-то будет')


def history(update, context):
    update.message.reply_text('тут позже что-то будет')


def error(update, context):
    update.message.reply_text('an error occured')


# function to handle normal text
def text(update, context):
    text_received = update.message.text
    if text_received == "Привет" or text_received == "/hello-world":
        update.message.reply_text(
            "Привет, я бот для удобного поиска отелей. Напиши /help, чтобы получить список команд")
    else:
        update.message.reply_text("Я тебя не понимаю. Напиши /help.")


def main():
    TOKEN = "5080367776:AAFkFZJhTOd1T92nAw-UJRD3uOF8SYPOivY"
    # create the updater, that will automatically create also a dispatcher and a queue to
    # make them dialoge
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("lowprice", lowprice))
    dispatcher.add_handler(CommandHandler("highprice", highprice))
    dispatcher.add_handler(CommandHandler("bestdeal", bestdeal))
    dispatcher.add_handler(CommandHandler("history", history))
    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    # add an handler for errors
    dispatcher.add_error_handler(error)
    # start your shiny new bot
    updater.start_polling()
    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
