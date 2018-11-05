import logging
import telegram
from telegram.ext import (Dispatcher, Filters, MessageHandler, CommandHandler, CallbackQueryHandler)
from flask import (Flask, request)
import settings
from handlers import *


class TelegramBot(APIHandlerMixin, BotHandlerMixin, Flask):
    TOKEN = settings.TOKEN
    API_URL = settings.API_URL
    APP_URL = settings.APP_URL
    DEFAULT = settings.DEFAULT

    
    def __init__(self, import_name):
        super(TelegramBot, self).__init__(import_name)
        self.route('/', methods=['POST'])(self.process_update)
        self.route('/set_webhook', methods=['GET'])(self.setWebhook)
        self.bot = telegram.Bot(self.TOKEN)
        self.dispatcher = self.setup()


    def setup(self):
        '''
        Set bot's handlers
        '''
        dispatcher = Dispatcher(self.bot, None, workers=0)

        dispatcher.add_handler(CommandHandler('start', self.start, pass_user_data=True))
        dispatcher.add_handler(CommandHandler('lang', self.lang))
        dispatcher.add_handler(CommandHandler('help', self.help))
        dispatcher.add_handler(CommandHandler('settings', self.settings, pass_user_data=True))
        dispatcher.add_handler(CallbackQueryHandler(self.put, pass_user_data=True))
        dispatcher.add_handler(MessageHandler(Filters.text, self.process_message, pass_user_data=True))
        
        return dispatcher


    def process_update(self):
        '''
        Get update from a chat and process it by handler
        '''
        self.update = telegram.update.Update.de_json(request.get_json(force=True), self.bot)
        logger.info(self.update)
        self.dispatcher.process_update(self.update)
        
        return 'OK'


    def setWebhook(self):
        '''
        Set webhook to APP_URL
        '''
        response = self.bot.setWebhook(webhook_url=self.APP_URL)

        return str(response)


app = TelegramBot(__name__)

logging.basicConfig(format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)