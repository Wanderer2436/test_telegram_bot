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


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Курс валют':
        course(message)
    elif message.text.strip() == 'Погода':
        a = bot.send_message(message.chat.id, "Введите название города: ")
        bot.register_next_step_handler(a, weather)
    elif message.text.strip() == 'Анекдот':
        joke(message)
    elif message.text.strip() == '/help':
        answer = 'Напишите /start чтобы вызвать меню или напишите:\nПогода\nКурс валют\nАнекдот '
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Извините, я не понимаю, напишите /help, чтобы посмотреть команды')