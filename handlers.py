import telebot
from telebot import types
from api_singleton import ApiSgltn
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date

class SearchRequest:
    def __init__(self, type: int, message: types.Message, bot: telebot.TeleBot, api_worker: ApiSgltn):
        self.__type = type
        self.__sity = ''
        self.__sity_id = 0
        self.__hotel_amount = 0
        self.__foto_flag = False
        self.__foto_amount = 0
        self.__date_in = ''
        self.__date_out = ''
        self.__user_id = message.from_user.id
        self.__bot = bot
        self.__api_worker = api_worker
        no_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "В каком городе искать отели?", reply_markup=no_keyboard)
        bot.register_next_step_handler(message, self.set_sity)

    def set_sity(self, message: types.Message):
        self.__sity = message.text
        answer = self.__api_worker.sity_request(self.__sity)
        if answer:
            self.__sity_id = answer
            self.__bot.send_message(message.from_user.id, 'Укажите дату заезда в формате гггг-мм-дд')
            self.__bot.register_next_step_handler(message, self.set_date_check_in)
        else:
            self.__bot.send_message(message.from_user.id, 'Ошибка в написании названия города.'
                                                          'Попроуйте ввести название города заново.')
            self.__bot.register_next_step_handler(message, self.set_sity)

    def set_date_check_in(self, message: types.Message):
        ######################## потом нужно получение даты выезда!######
        data = message.text
        self.__bot.send_message(message.from_user.id, 'Сколько отелей вывести в результате поиска? (не более 10)')
        self.__bot.register_next_step_handler(message, self.set_hotel_amount)


    def set_hotel_amount(self, message: types.Message):
        self.__hotel_amount = int(message.text)
        if self.__hotel_amount > 10 or self.__hotel_amount < 1:
            self.__bot.send_message(message.from_user.id, 'Указано не верное количество отелей. '
                                                          'Можно запросить от 1 до 10')
            self.__bot.register_next_step_handler(message, self.set_hotel_amount)
        else:
            self.__bot.send_message(message.from_user.id, 'Включать в результаты поиска фото отелей? '
                                                          '(да/нет)')
            self.__bot.register_next_step_handler(message, self.set_foto_flag)

    def set_foto_flag(self, message: types.Message):
        self.__foto_flag = message.text
        if self.__foto_flag.lower() == 'да':
            self.__bot.send_message(message.from_user.id, 'Укажите количетсво фотографий для каждого отеля (от 1 до 10)')
            self.__bot.register_next_step_handler(message, self.set_foto_amount)
        elif self.__foto_flag.lower() == 'нет':
            ######################################################
            ###### корректировать!! ##
            # отдельный метод на отправку результатов ##########
            ##################################################
            answer = self.result_func()
            self.__bot.send_message(message.from_user.id, answer)
        else:
            self.__bot.send_message(message.from_user.id, 'Некорректный ввод. Напишите да или нет.')
            self.__bot.register_next_step_handler(message, self.set_foto_flag)

    def set_foto_amount(self, message: types.Message):
        self.__foto_amount = int(message.text)
        if self.__foto_amount > 10 or self.__foto_amount < 1:
            self.__bot.send_message(message.from_user.id,
                                'Указано не верное количество фотографий. Можно запросить от 1 до 10')
            self.__bot.register_next_step_handler(message, self.set_foto_amount)
        else:
            answer = self.result_func()
            self.__bot.send_message(message.from_user.id, answer)

    def get_req_info(self):
        return [self.__sity_id, self.__hotel_amount, self.__type]

    def result_func(self):
        data = self.get_req_info()
        return self.__api_worker.get_results(data[0], data[1], data[2])

