import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class ExchangeConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}. Введите верное значение.')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту{quote}. Введите верное значение.')

    try:
            base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту{quote}. Введите верное значение.')

    try:
            amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Не удалось обработать количество{amount}')


    quote_ticker, base_ticker = keys[quote], keys[base]
    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
    total_base = json.loads(r.content)[keys[base]]