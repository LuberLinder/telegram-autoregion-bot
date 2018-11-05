import requests


class APIHandlerMixin:
    API_URL = None

    
    def api_get_codes(self, code, country_id=None, lang_id=None):
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