from settings import TOKEN, headers
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import sqlite3


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Курс валют")
    item2 = types.KeyboardButton("Погода")
    item3 = types.KeyboardButton("Анекдот")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id, 'Чего желаете?', reply_markup=markup)

