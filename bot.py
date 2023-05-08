import asyncio
import logging
from bs4 import BeautifulSoup
import requests
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater, CallbackContext

url = 'https://myfin.by/converter'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, features="html.parser")
html = soup.prettify("utf-8")

if response.status_code == 200:
    def get_dollar():
        exchange_data = soup.find_all('div', class_='record vis_bestmbusd')
        dollar_exchange_data = str(exchange_data).split(sep='value=')[-1].split("/")[0].split('"')[1]
        return dollar_exchange_data


    def get_euro():
        exchange_data = soup.find_all('div', class_='record vis_bestmbeur')
        euro_exchange_data = str(exchange_data).split(sep='value=')[-1].split("/")[0].split('"')[1]
        return euro_exchange_data


    def get_gbp():
        exchange_data = soup.find_all('div', class_='record vis_bestmbgbp')
        gbp_exchange_data = str(exchange_data).split(sep='value=')[-1].split("/")[0].split('"')[1]
        return gbp_exchange_data


    def get_cny():
        exchange_data = soup.find_all('div', class_='record vis_bestmbcny')
        cny_exchange_data = str(exchange_data).split(sep='value=')[-1].split("/")[0].split('"')[1]
        return cny_exchange_data


    def get_rub():
        exchange_data = soup.find_all('div', class_='record vis_bestmbrub')
        rub_exchange_data = str(exchange_data).split(sep='value=')[-1].split("/")[0].split('"')[1]
        return rub_exchange_data

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
TELEGRAM_BOT_TOKEN = '6043524872:AAHbOvk9AlQx4CW_Fv20zgNBV8iNz9F8pIE'


def start_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton('Доллар', callback_data='button1'),
         InlineKeyboardButton('Евро', callback_data='button2'),
         InlineKeyboardButton('Юань', callback_data='button3')],
        [InlineKeyboardButton('Фунт', callback_data='button5'),
         InlineKeyboardButton('Рубль', callback_data='button4')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите валюту для парсинга', reply_markup=reply_markup)


def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'button1':
        query.message.reply_text(f'1$ равен {get_dollar()}$')
    elif query.data == 'button2':
        query.message.reply_text(f'1$ равен {get_euro()} евро')
    elif query.data == 'button3':
        query.message.reply_text(f'1$ равен {get_cny()} юань')
    elif query.data == 'button4':
        query.message.reply_text(f'1$ равен {get_rub()} рублей')
    elif query.data == 'button5':
        query.message.reply_text(f'1$ равен {get_gbp()} фунтов')


def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start_command)
    button_handler = CallbackQueryHandler(button_click)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_handler)

    updater.start_polling()
    logger.info('Started the bot.')

    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    asyncio.run(main())
