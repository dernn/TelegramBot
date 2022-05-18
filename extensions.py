import requests
import json
from config import keys


# list of tickers needed >>> !!!

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(request):

        if len(request) > 3:
            raise APIException('Too many entries here. Please, use the default mask: <from> <to> <how much>')

        quote = request[0]

        try:
            quote = keys[quote]
        except KeyError:
            raise APIException(f'What do you mean *\{quote}*?')

        try:
            base = request[1]
        except IndexError:
            base = 'dollar'

        try:
            base = keys[base]
        except KeyError:
            raise APIException(f'What do you mean *\{base}*?')

        try:
            amount = request[2]
        except IndexError:
            amount = 1

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'And how should I count *\{amount}*?')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        answer = f'{json.loads(r.content)[base.upper()] * float(amount)} {base.upper()}'

        return answer
