import requests
import json
from config import headers

url = "https://api.apilayer.com/exchangerates_data/symbols"

response = requests.get(url, headers=headers, data={})
answer = json.loads(response.content)['symbols']

keys = json.loads(response.content)['symbols']

currencies = [key for key in answer]


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(request):

        if len(request) > 3:
            raise APIException('Too many entries here. Please, use the default mask: <from> <to> <how much>')

        quote = request[0]

        quote = quote.upper()
        if quote not in currencies:
            raise APIException(f'What do you mean *\{quote}*?')

        try:
            base = request[1]
        except IndexError:
            base = 'USD'

        base = base.upper()
        if base not in currencies:
            raise APIException(f'What do you mean *\{base}*?')

        try:
            amount = request[2]
        except IndexError:
            amount = 1

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'And how should I count *\{amount}*?')

        r = requests.get(f'https://api.apilayer.com/exchangerates_data/convert?to={base}&from={quote}&amount={amount}',
                         headers=headers, data={})

        answer = f'{json.loads(r.content)["result"]} {base}'

        return answer

    @staticmethod
    def splitter(text):
        stext = []
        mark = text.find('#', 4064)
        stext.append(text[:mark])
        stext.append(text[mark:])

        return stext
