import telebot
from config import keys, TOKEN
from utils import ConvertionException, ExchangeConverter

bot = telebot.TeleBot(TOKEN)

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
    try:
        values = message.text.split(' ')

        if len(values) > 4:
            raise ConvertionException('Много парметров.')

        quote, base, amount = values
        total_base = ExchangeConverter.convert(quote,base,amount)

        text = f'Переводим {base} в {quote}\n{amount} у.е. = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

