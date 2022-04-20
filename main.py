import os
import telebot
from dotenv import load_dotenv
from telebot import types
from api_singleton import ApiSgltn
from handlers import SearchRequest
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN", "Put here your token"))


@bot.message_handler(commands=["start"])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Я на связи. Для получения списка команд напишите /help')


@bot.message_handler(commands=["help"])
def help(message, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/help")
    item2 = types.KeyboardButton("/lowprice")
    item3 = types.KeyboardButton("/highprice")
    item4 = types.KeyboardButton("/bestdeal")
    item5 = types.KeyboardButton("/history")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Список команд:\n"
                                      "/help — помощь по командам бота,\n"
                                      "/lowprice — вывод самых дешёвых отелей в городе,\n"
                                      "/highprice — вывод самых дорогих отелей в городе,\n"
                                      "/bestdeal — вывод отелей, наиболее подходящих по цене "
                                      "и расположению от центра.\n"
                                      "/history — вывод истории поиска отелей\n", reply_markup=markup)


@bot.message_handler(commands=["lowprice"])
def lowprice(message, res=False):
    SearchRequest(0, message, bot, ApiSgltn())


@bot.message_handler(commands=["highprice"])
def highprice(message, res=False):
    no_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Позже тут что-то будет", reply_markup=no_keyboard)


@bot.message_handler(commands=["bestdeal"])
def bestdeal(message, res=False):
    no_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Позже тут что-то будет", reply_markup=no_keyboard)


@bot.message_handler(commands=["history"])
def history(message, res=False):
    no_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Позже тут что-то будет", reply_markup=no_keyboard)

@bot.message_handler(commands=["calendar"])
def calendar_key(message):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    text_received = message.text
    if text_received == "Привет" or text_received == "/hello-world":
        bot.send_message(message.chat.id, "Привет, я бот для удобного поиска отелей. "
                                          "Напиши /help, чтобы получить список команд")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
