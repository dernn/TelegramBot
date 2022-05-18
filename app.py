import telebot
from extensions import CryptoConverter, APIException, keys
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello, {message.chat.username}!')
    bot.send_message(message.chat.id, f'''I am a humble currency bot\.
I can convert some currencies between themselves\.
Use the following mask: _\\<from\> \<to\> \<how much\>_
For _\\<from\>_ and _\\<to\>_ use standard tickers \(see /values\)\.

_\\Example:_ usd eur 200


Commands \(that's all I can\):

\# /help \- to repeat this message
\# /zen \- to get a pause and meditate''', parse_mode='MarkdownV2')


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, f'''Use the following mask: _\\<from\> \<to\> \<how much\>_
For _\\<from\>_ and _\\<to\>_ use standard tickers \(see /values\)\.

_\\Example:_ usd eur 200


Commands \(that's all I can\):

\# /help \- to repeat this message
\# /zen \- to get a pause and meditate''', parse_mode='MarkdownV2')


@bot.message_handler(commands=['values'])
def values(message):
    text = f"List of currencies:"
    for key, value in keys.items():
        text += f'\n# {key} : {value}'
    if len(text) > 4096:
        text = CryptoConverter.splitter(text)

        bot.send_message(message.chat.id, text[0])
        bot.send_message(message.chat.id, text[1])
    else:
        bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['zen'])
def zen(message):
    bot.send_message(message.chat.id, 'Unfocused your mind and do nothing...')


@bot.message_handler(content_types=['text'])
def convert(message):
    request = message.text.split()

    try:
        answer = CryptoConverter.get_price(request)
    except APIException as msg:
        bot.send_message(message.chat.id, f'{msg}', parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, f'''Try using default mask: _\\<from\> \<to\> \<how much\>_
See also list of available tickers /values''', parse_mode='MarkdownV2')
    except Exception as msg:
        bot.send_message(message.chat.id, 'Something wrong in my code')
        bot.send_message(message.chat.id, f'{msg}', parse_mode='MarkdownV2')
        bot.send_message(message.chat.id, '_\\To understand and to forgive._', parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling(non_stop=True)
