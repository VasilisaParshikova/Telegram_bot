import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Помощь по командам бота"),
    ('history', 'Вывод истории поиска отелей'),
    ('lowprice', 'Вывод самых дешёвых отелей в городе'),
    ('highprice', 'Вывод самых дорогих отелей в городе'),
    ('beastdeal', 'Вывод отелей, наиболее подходящих по цене и расположению от центра'),
)
