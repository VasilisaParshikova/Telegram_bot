import os
import requests
import json
import telebot
from dotenv import load_dotenv
from telebot import types

load_dotenv()
headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPID_API_KEY", "")
}


bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN", "Put here your token"))


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Для получения списка команд напишите /help')


@bot.message_handler(commands=["help"])
def help(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/help")
    item2 = types.KeyboardButton("/lowprice")
    item3 = types.KeyboardButton("/highprice")
    item4 = types.KeyboardButton("/bestdeal")
    item5 = types.KeyboardButton("/history")
    markup.add(item1, item2, item3, item4, item5)
    bot.send_message(m.chat.id, "Список команд:\n"
                                "/help — помощь по командам бота,\n"
                                "/lowprice — вывод самых дешёвых отелей в городе,\n"
                                "/highprice — вывод самых дорогих отелей в городе,\n"
                                "/bestdeal — вывод отелей, наиболее подходящих по цене "
                                "и расположению от центра.\n"
                                "/history — вывод истории поиска отелей\n", reply_markup=markup)


sity = ''
sity_id = 0
hotel_amount = 0
foto_flag = False
foto_amount = 0;


@bot.message_handler(commands=["lowprice"])
def lowprice(message, res=False):
    no_keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "В каком городе искать отели?", reply_markup=no_keyboard)
    bot.register_next_step_handler(message, get_sity)


def get_sity(message):
    global sity
    global sity_id
    sity = message.text
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": sity}
    response = requests.request("GET", url, headers=headers, params=querystring)
    sity_dict = json.loads(response.text)
    if len(sity_dict['suggestions'][0]['entities']) == 0:
        bot.send_message(message.from_user.id, 'Ошибка в написании названия города.'
                                               'Попроуйте ввести название города заново.')
        bot.register_next_step_handler(message, get_sity)
    else:
        sity_id = sity_dict['suggestions'][0]['entities'][0]['destinationId']
        bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате поиска? (не более 10)')
        bot.register_next_step_handler(message, get_hotel_amount)


def get_hotel_amount(message):
    global hotel_amount
    hotel_amount = int(message.text)
    if hotel_amount > 10 or hotel_amount < 1:
        bot.send_message(message.from_user.id, 'Указано не верное количество отелей. Можно запросить от 1 до 10')
        bot.register_next_step_handler(message, get_hotel_amount)
    else:
        bot.send_message(message.from_user.id, 'Включать в результаты поиска фото отелей? (да/нет)')
        bot.register_next_step_handler(message, get_foto_flag)


def get_foto_flag(message):
    global foto_amount
    global foto_flag
    foto_flag = message.text
    if foto_flag.lower() == 'да':
        bot.send_message(message.from_user.id, 'Укажите количетсво фотографий для каждого отеля (от 1 до 10)')
        bot.register_next_step_handler(message, get_foto_amount)
    elif foto_flag.lower() == 'нет':
        foto_amount = 0
        answer = result_func()
        bot.send_message(message.from_user.id, answer)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод. Напишите да или нет.')
        bot.register_next_step_handler(message, get_foto_flag)


def get_foto_amount(message):
    global foto_amount
    foto_amount = int(message.text)
    if foto_amount > 10 or foto_amount < 1:
        bot.send_message(message.from_user.id, 'Указано не верное количество фотографий. Можно запросить от 1 до 10')
        bot.register_next_step_handler(message, get_foto_amount)
    else:
        answer = result_func()
        bot.send_message(message.from_user.id, answer)


def result_func():
    global foto_amount
    global hotel_amount
    global sity
    global sity_id


    # bot.send_message(message.from_user.id, 'Необходимо найти {} отелей в городе {}.'
    #                                       'Результаты поика отсортировать по увеличению цены.'
    #                                       'Для каждого отеля выводить {} фотографий'.format(
    #    hotel_amount, sity, foto_amount
    # ))
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("RAPID_API_KEY", "")
    }
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": sity_id, "pageNumber": "1", "pageSize": str(hotel_amount), "checkIn": "2020-02-02",
                   "checkOut": "2020-02-15", "adults1": "1", "sortOrder": "PRICE"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    hotels_dict = json.loads(response.text)
    hotels_dict = hotels_dict['data']['body']['searchResults']['results']
    results = []
    hotel_id_in_res = 0
    for hotel_info in hotels_dict:
        results.append(dict())
        results[hotel_id_in_res]['name'] = hotel_info['name']
        results[hotel_id_in_res]['starRating'] = hotel_info['starRating']
        results[hotel_id_in_res]['address'] = hotel_info['address']['streetAddress']
        #    results[hotel_id_in_res]['guestRating'] = hotel_info['guestReviews']['rating']
        results[hotel_id_in_res]['price'] = hotel_info['ratePlan']['price']['current']
        hotel_id_in_res += 1
    answer = []

    for hotel in results:
        answer.append('Отель {} {} звезды.\nАдрес:{}.\nЦена {}\n'.format(
            hotel['name'], hotel['starRating'], hotel['address'], hotel['price']
        ))
    answer = ''.join(answer)
    return answer




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


@bot.message_handler(content_types=["text"])
def handle_text(message):
    text_received = message.text
    if text_received == "Привет" or text_received == "/hello-world":
        bot.send_message(message.chat.id, "Привет, я бот для удобного поиска отелей. "
                                          "Напиши /help, чтобы получить список команд")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
