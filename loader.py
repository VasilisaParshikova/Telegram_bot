import telebot
from config_data import config

storage = telebot.storage.StateMemoryStorage()
bot = telebot.TeleBot(token=config.BOT_TOKEN, state_storage=storage)
