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


def weather(message):
    try:
        city = message.text
        city = city + " weather"
        city = city.replace(" ", "+")
        res = requests.get(
            f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid'
            f'=chrome&ie=UTF-8', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        wind = soup.select('#wob_ws')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        answer = location + '\n' + time + '\n' + info + '\n' + wind + '\n' + weather + "°C"
    except Exception:
        answer = "Город не найден, попробуйте еще раз"
    bot.send_message(message.chat.id, answer)
    start(message)


def course(message):
    response = requests.get('https://ru.investing.com/currencies/usd-rub')
    bs = BeautifulSoup(response.text, "lxml")
    dollar = bs.find('span', class_="text-2xl")
    response2 = requests.get('https://ru.investing.com/currencies/eur-rub')
    bs2 = BeautifulSoup(response2.text, "lxml")
    euro = bs2.find('span', class_="text-2xl")
    ans = 'Курс доллара: ' + str(dollar.text) + '\n' + 'Курс евро: ' + str(euro.text)
    bot.send_message(message.chat.id, ans)


bot.polling(none_stop=True, interval=0)