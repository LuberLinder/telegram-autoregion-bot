import requests
from flask import (Flask, request, json)
import settings

class BotHandlerMixin:  
    BOT_URL = None

    def get_chat_id(self, data):
        '''
        Method to extract chat id from telegram request.
        '''
        return data['message']['chat']['id']

    def get_message(self, data):
        '''
        Method to extract message id from telegram request.
        '''
        return data['message']['text']

    def send_message(self, data):
        '''
        Prepared data should be json which includes at least `chat_id` and `text`
        '''       
        url = self.BOT_URL + 'sendMessage'
        requests.post(url, data=data)

    def set_webhook(self, data):
        '''
        Prepared data should be json which includes at least `chat_id` and `text`
        '''       
        url = self.BOT_URL + 'setWebhook'
        response = requests.post(url, data=data)
        
        return response

class APIHandlerMixin:
    API_URL = None
    
    def get_codes(self, code, country_id=1, lang_id=3):
        '''
        Make a request to the REST API's <codes> endpoint
        '''
        url = self.API_URL + 'codes'
        payload = {
            'country_id': country_id,
            'code': code,
            'lang_id': lang_id,
        }
        response = requests.get(url, params=payload)

        return response.json()


class TelegramBot(BotHandlerMixin, APIHandlerMixin, Flask):  
    BOT_URL = settings.BOT_URL
    API_URL = settings.API_URL

    def __init__(self, import_name):
        super(TelegramBot, self).__init__(import_name)
        self.route('/', methods=['POST'])(self.post_handler)
        self.route('/set_webhook', methods=['GET'])(self.webhook_handler)

    def prepare_data_for_answer(self, data):
        '''
        Get a message from the chat and prepare a response on it.
        A vehicle registration plate region code of the selected country
        expected as the massage and a name of corresponding municipality
        should be send back as the answer (or 'Not found' text) 
        '''
        answer = ''
        message = self.get_message(data)
        chat_id = self.get_chat_id(data)
        response = self.get_codes(message)
        
        for r in response:
            try:
                answer += f"{r['code']}: {r['name']} ({', '.join(r['cities'])})\n"
            except:
                # todo: logging should be here
                pass
        
        if not answer:
            answer = 'Not found'

        payload = {
            'chat_id': chat_id,
            'text': answer,
        }

        return payload

    def post_handler(self):
        '''
        Handler for the root url ('/'). 
        Get a massage, prepare data for an answer, send the answer
        '''
        data = request.get_json()
        answer_data = self.prepare_data_for_answer(data)
        self.send_message(answer_data)

        return 'ok!'

    def webhook_handler(self):
        '''
        Set webhook to application url in order to activate the bot
        '''
        payload = {
            'url': settings.APP_URL,
            'allowed_updates': ['message'],
        }
        response = self.set_webhook(payload)

        return 'Result: ' + json.dumps(response.json())

app = TelegramBot(__name__)