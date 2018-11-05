from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)


class BotHandlerMixin:
    DEFAULT = None

    
    def lang(self, bot, update):
        '''
        Show language menu
        '''
        keyboard = [[InlineKeyboardButton('Српски', callback_data='lang_id=1'),
                     InlineKeyboardButton('Srpski', callback_data='lang_id=2')],
                    [InlineKeyboardButton('Русский', callback_data='lang_id=3')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Please choose your language:', reply_markup=reply_markup)


    def start(self, bot, update, user_data):
        '''
        Set default settings
        '''
        user_data.update(self.DEFAULT)
        update.message.reply_text('Initial settings was set')


    def help(self, bot, update):
        '''
        Print help text
        '''
        reply_text = '''
            Type one- or two-letter code to see the info.
            \nSearch is available only for Serbia for now.
            \nUse /lang to set a language.
            \nUse /settings to see current settings.
            \nUse /start to reset settings to default.
            '''
        update.message.reply_text(reply_text)


    def settings(self, bot, update, user_data):
        '''
        Show current settings
        '''
        if not user_data:
            user_data.update(self.DEFAULT)
        
        reply_text = ''
        for key, value in user_data.items():
            reply_text += f'{key}: {value}\n'

        update.message.reply_text(reply_text)


    def put(self, bot, update, user_data):
        '''
        Save user settings
        '''
        query = update.callback_query
        key, _, value = query.data.partition('=')
            
        user_data[key] = value
        bot.editMessageText(
            f'Selected option: {key}: {value}', 
            chat_id=query.message.chat_id, 
            message_id=query.message.message_id
        )


    def process_message(self, bot, update, user_data):
        '''
        Redirect a message from the chat to REST API 
        and produce a response back to the chat
        '''
        reply_text = ''
        
        code = update['message']['text']
        country_id = user_data.get('country_id', self.DEFAULT['country_id'])
        lang_id = user_data.get('lang_id', self.DEFAULT['lang_id'])
        
        response = self.api_get_codes(code, country_id=country_id, lang_id=lang_id)
        
        for r in response:
            try:
                reply_text += f'{r["code"]}: {r["name"]} ({", ".join(r["cities"])})\n'
            except:
                pass
        
        if not reply_text:
            reply_text = 'Not found'

        update.message.reply_text(reply_text)