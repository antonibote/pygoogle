__author__ = 'antonibote'
from urllib.parse import quote
import requests
import re,json
from .utils import user_agents
import os
from http.cookiejar import LWPCookieJar
import random

class GTranslate:
    DOMAIN = "translate.googleapis.com"

    def __init__(self, domain = None, agents = None, lang="en", use_cookie=None):
        if domain is None:
            domain = GTranslate.DOMAIN
        if agents is None:
            agents = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
        self._agent = agents
        self._lang = lang
        self._domain = domain
        self._use_cookie = use_cookie
        self._session = requests.Session()
        if not use_cookie: #use_browser_cookie is None
            home_folder = os.getenv('HOME')
            if not home_folder:
                home_folder = os.getenv('USERHOME')
                if not home_folder:
                    home_folder = '.'   # Use the current folder on error.
            self._cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
            self._session.cookies = self._cookie_jar
            try:
                self._cookie_jar.load()
            except Exception:
                pass
        else:
            self._cookie_jar = None

    def __call__(self, message, lang_to='en', lang_from="auto", raw=False):
        """
        crawl google translate.
        :param message: text
        :param lang_to: dst lang
        :param lang_from: src lang
        :param raw: whether return raw response
        :return: result
        """
        if self._use_cookie:
            self._cookie_jar = random.choice(self._use_cookie)
        if lang_to not in languages:
            raise Exception("Language %s is not supported as lang_to." % lang_to)
        if lang_from not in languages and lang_from != 'auto':
            raise Exception("Language %s is not supported as lang_from." % lang_from)
        message = quote(message)
        url = self.translate_url(message, lang_from, lang_to)
        data = json.loads(re.sub(r"(,|\[)(?=,|])", "\\1 null", self.page(url)))
        if raw:
            return data
        return dict(res = self._res(data),
                    lang_detect = self._lang_detect(data),
                    ref = self._ref(data),
                    example=self._example(data),
                    pos=self._pos(data),
                    tpos=self._transed_pos(data)
                    )

    def _res(self, data):
        return data[0]

    def _lang_detect(self, data):
        return [(x,v) for x,v in zip(data[8][0],data[8][2])]

    def _ref(self, data):
        return data[14]

    def _example(self, data):
        return data[13]

    def _pos(self, data):
        p = data[12]
        if p is None:
            return {}
        return {x[0]: x[1] for x in p}

    def _transed_pos(self, data):
        p = data[1]
        if p is None:
            return {}
        return {x[0]: x[1] for x in p}

    def page(self, url,debug =False):
        agent = str(self._agent)
        if debug:
            print("user-agent:%s" % agent)
        if self._use_cookie:
            res = self._session.get(url, headers = {'User-Agent': agent}, cookies = self._cookie_jar,verify=False)
        else:
            res = self._session.get(url, headers = {'User-Agent': agent},verify=False)
        return res.text

    def translate_url(self, txt, f, t):
        return "http://%s/translate_a/single?client=gtx&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&dt=at&sl=%s&tl=%s&q=%s" % (self._domain, f, t, txt)

languages = {
  'af': 'Afrikaans',
  'sq': 'Albanian',
  'am': 'Amharic',
  'ar': 'Arabic',
  'hy': 'Armenian',
  'az': 'Azerbaijani',
  'eu': 'Basque',
  'be': 'Belarusian',
  'bn': 'Bengali',
  'bh': 'Bihari',
  'bg': 'Bulgarian',
  'my': 'Burmese',
  'ca': 'Catalan',
  'chr': 'Cherokee',
  'zh': 'Chinese',
  'zh-CN': 'Chinese_simplified',
  'zh-TW': 'Chinese_traditional',
  'hr': 'Croatian',
  'cs': 'Czech',
  'da': 'Danish',
  'dv': 'Dhivehi',
  'nl': 'Dutch',
  'en': 'English',
  'eo': 'Esperanto',
  'et': 'Estonian',
  'tl': 'Filipino',
  'fi': 'Finnish',
  'fr': 'French',
  'gl': 'Galician',
  'ka': 'Georgian',
  'de': 'German',
  'el': 'Greek',
  'gn': 'Guarani',
  'gu': 'Gujarati',
  'iw': 'Hebrew',
  'hi': 'Hindi',
  'hu': 'Hungarian',
  'is': 'Icelandic',
  'id': 'Indonesian',
  'iu': 'Inuktitut',
  'ga': 'Irish',
  'it': 'Italian',
  'ja': 'Japanese',
  'kn': 'Kannada',
  'kk': 'Kazakh',
  'km': 'Khmer',
  'ko': 'Korean',
  'ku': 'Kurdish',
  'ky': 'Kyrgyz',
  'lo': 'Laothian',
  'lv': 'Latvian',
  'lt': 'Lithuanian',
  'mk': 'Macedonian',
  'ms': 'Malay',
  'ml': 'Malayalam',
  'mt': 'Maltese',
  'mr': 'Marathi',
  'mn': 'Mongolian',
  'ne': 'Nepali',
  'no': 'Norwegian',
  'or': 'Oriya',
  'ps': 'Pashto',
  'fa': 'Persian',
  'pl': 'Polish',
  'pt-PT': 'Portuguese',
  'pa': 'Punjabi',
  'ro': 'Romanian',
  'ru': 'Russian',
  'sa': 'Sanskrit',
  'sr': 'Serbian',
  'sd': 'Sindhi',
  'si': 'Sinhalese',
  'sk': 'Slovak',
  'sl': 'Slovenian',
  'es': 'Spanish',
  'sw': 'Swahili',
  'sv': 'Swedish',
  'tg': 'Tajik',
  'ta': 'Tamil',
  'tl': 'Tagalog',
  'te': 'Telugu',
  'th': 'Thai',
  'bo': 'Tibetan',
  'tr': 'Turkish',
  'uk': 'Ukrainian',
  'ur': 'Urdu',
  'uz': 'Uzbek',
  'ug': 'Uighur',
  'vi': 'Vietnamese',
  'cy': 'Welsh',
  'yi': 'Yiddish'
};

if __name__ == '__main__':
    t = GTranslate()
    for k,v in t("you",lang_to="zh-CN").items():
        print(k)
        print(v)