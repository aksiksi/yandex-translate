import json
import requests
from multiprocessing import Pool


def make_api_request(url):
    result = json.loads(requests.get(url).text)

    if result['code'] != 200:
        raise YandexTranslatorException('Check your API key. Or maybe the API itself is down.')

    return result['text'][0]


class YandexTranslatorException(Exception):
    pass


class YandexTranslator(object):
    '''
        A thin wrapper around the Yandex Translation API.

        Arguments:
            - api_key (string)
            - from_lang - two-letter language specifier i.e. "en" or "ar" (string)
            - to_lang (string)
            - list of strings to translate (optional)

        Methods:
            - update_languages: updates `self.languages` to reflect supported translation pairs (locale='en' -> None)
            - translate: translate the current strings (-> None)
            - make_dict: Combines input strings and translated version into a dictionary (-> dict)
    '''
    def __init__(self, api_key, from_lang, to_lang, strings=None):
        self.api_key = api_key
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.strings = [] if not strings else strings
        self.translated = []
        self.languages = []
        self.api_url = u'https://translate.yandex.net/api/v1.5/tr.json/translate?'

    def update_languages(self, locale='en'):
        self.languages = requests.get('https://translate.yandex.net/api/v1.5/tr.json/getLangs?key={0}&ui={1}'
                                 .format(self.api_key, locale)).json()['dirs']

    def translate(self):
        p = Pool(5)
        urls = []

        for string in self.strings:
            data = u'key={0}&lang={1}&text={2}'.format(
                self.api_key,
                '{0}-{1}'.format(self.from_lang, self.to_lang),
                string.replace(' ', '+')
            )

            urls.append(self.api_url + data)

        for s in p.map(make_api_request, urls):
            self.translated.append(s)

    def make_dict(self):
        out = {}

        if len(self.strings) == len(self.translated):
            for k, v in zip(self.strings, self.translated):
                out[k] = v
        else:
            raise YandexTranslatorException('List size mismatch.')

        return out
