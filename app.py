import telebot
import requests
import json

TOKEN = "1599342418:AAF_r4fxNFAfz9Lu_WTzg0V9-t8n-VK86TE"

bot = telebot.TeleBot(TOKEN)

keys = {
    'доллар''USD'
    'рубль''RUR'
    'швейцарский франк''CHF'
}

class ConvertionsException(Exception):
    pass

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Что бы сконвертировать валюту, дайте команду боту в следующем формате: \n <тикер валюты> \
<в какую валюту конвертировать> \
<объём конвертруемой валюты>\n Что бы увидель список всех доступных валют для конвертации введите команду: /values "
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) > 3:
        raise ConvertionsException('Много парметров.')

    quote, base, amount = values

    if quote == base:
        raise ConvertionsException(f'Невозможно конвертировать одинаковык валюты {base}. Введите верное значение.')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionsException(f'Не удалось обработать валюту{quote}')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionsException(f'Не удалось обработать валюту{quote}')

    try:
            amount = float(amount)
    except ValueError:
        raise ConvertionsException(f'Не удалось обработать количество{amount}')

    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
    total_base = json.loads(r.content)[dict[base]]
    text = f'Цена {amount} {quote} в {base} = {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)


