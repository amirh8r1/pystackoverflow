import os

import telebot
from telebot import apihelper

apihelper.ENABLE_MIDDLEWARE = True

# initialize bot
bot = telebot.TeleBot(
    os.environ['TELEGRAM_BOT_TOKEN'], parse_mode='HTML'
)
