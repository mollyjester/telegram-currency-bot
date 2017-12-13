import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import urllib.request as request
import currency
import datetime


class CurrencyBotRU:
    command_start = 'start'
    command_help = 'help'
    command_list = 'list'
    command_find = 'f'
    currency_item_format = '%s <b>%s</b> [<b>%s</b>]: %s'

    def __init__(self, token):
        self._currency_list = []
        self.cache_date = datetime.date.today()

        self.updater = Updater(token=token)

        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler(self.command_start, self._handle_start))
        self.dispatcher.add_handler(CommandHandler(self.command_help, self._handle_help))
        self.dispatcher.add_handler(CommandHandler(self.command_list, self._handle_list))
        self.dispatcher.add_handler(CommandHandler(self.command_find, self._handle_find, pass_args=True))

    @property
    def currency_list(self):
        today = datetime.date.today()
        if (not self._currency_list
                or self.cache_date != today):
            response = request.urlopen(currency.url_currency, timeout=10)
            cp = currency.CurrencyParser(response.read())
            self._currency_list = cp.parse()
            self.cache_date = today
        return self._currency_list

    @staticmethod
    def make_list_text(items):
        text = '\n'.join(
            [CurrencyBotRU.currency_item_format % (x.nominal, x.name, x.charcode, x.rate)
             for x in items])
        return text

    def start(self):
        self.updater.start_polling()

    def _handle_start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Я бот, показывающий курсы валют. Напишите /help для списка доступных комманд.")

    def _handle_help(self, bot, update):
        text = '\n'.join(
            ('Доступные команды:',
             '/start, /help - начать работу, получить список команд',
             '/list - список актуальных курсов валют',
             '/f - найти и вывести валюту по названию или коду'))
        bot.send_message(chat_id=update.message.chat_id,
                         text=text)

    def _handle_list(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=CurrencyBotRU.make_list_text(self.currency_list[1:]),
                         parse_mode=telegram.ParseMode.HTML)

    def _handle_find(self, bot, update, args):
        if args:
            searchfor = ''.join(args).upper()
            currencies = [x for x in self.currency_list[1:] if searchfor in str(x).upper()]
        else:
            currencies = self.currency_list[1:]

        if currencies:
            text = CurrencyBotRU.make_list_text(currencies)
        else:
            text = 'Ничего не найдено'
        bot.send_message(chat_id=update.message.chat_id,
                         text=text,
                         parse_mode=telegram.ParseMode.HTML)


if __name__ == '__main__':
    resp = request.urlopen(currency.url_currency, timeout=10)
    parser = currency.CurrencyParser(resp.read())
    cur_items = parser.parse()
    curs = [x for x in cur_items[1:] if 'доллар' in str(x)]
    print(CurrencyBotRU.make_list_text(curs))
