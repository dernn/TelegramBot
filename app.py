import telebot
from extensions import CryptoConverter, APIException
from config import TOKEN, currencies

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.chat.username}!')
    bot.send_message(message.chat.id, f'''I am a humble currency bot.
I can convert some currencies between themselves.
Use the following mask: <from> <to> <how much>
For <from> and <to> can use standard tickers.

Example: usd eur 200


Commands (that's all I can):

# /help - to repeat this message
# /values - to show available currency list
# /zen - to get a pause and meditate''')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, f'''Use the following mask: <from> <to> <how much>
For <from> and <to> can use standard tickers.

Example: usd eur 200


Commands (that's all I can):

# /help - to repeat this message
# /values - to show available currency list
# /zen - to get a pause and meditate''')


@bot.message_handler(commands=['values'])
def values(message):
    text = "List of currencies:"
    for key in currencies:
        text += f'\n# {key}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['zen'])
def zen(message):
    bot.send_message(message.chat.id, 'Unfocused your mind and do nothing')


@bot.message_handler(content_types=['text'])
def convert(message):
    request = message.text.split()

    try:
        answer = CryptoConverter.get_price(request)
    except APIException as msg:
        bot.send_message(message.chat.id, f'{msg}', parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, f'Try using default mask: _\\<from\> \<to\> \<how much\>_', parse_mode='MarkdownV2')
    except Exception as msg:
        bot.send_message(message.chat.id, 'Something wrong in my code')
        bot.send_message(message.chat.id, f'{msg}', parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, '_\\To understand and to forgive._', parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling(non_stop=True)
