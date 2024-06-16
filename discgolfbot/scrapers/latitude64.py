import time
from disc.disc import Disc
from .scraper import Scraper
import re
import requests
import json

class Latitude64(Scraper):
    def __init__(self):
        super().__init__()
        self.name = 'store.latitude64.se'
        self.url = 'https://store.latitude64.se'


class DiscScraper(Latitude64):
    def __init__(self, search):
        super().__init__()
        self.search = search
        self.scrape_url = f'https://store.latitude64.se/pages/search-results-page?q={search}&page=1&rb_stock_status=In%20Stock'
        self.discs = []

    def scrape(self):
        start_time = time.time()
        soup = self.urllib_get_beatifulsoup()
        script_search_api = soup.find('script', src=re.compile(
            r'//searchserverapi\.com/widgets/shopify/init\.js\?a=.*'))
        api_key = script_search_api['src'].split('=')[1]

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Referer': 'https://store.latitude64.se/',
        }

        params = {
            'api_key': api_key,
            'q': self.search,
            'sortBy': 'created',
            'sortOrder': 'desc',
            'restrictBy[stock_status]': 'In Stock',
            'startIndex': '0',
            'maxResults': '15',
            'items': 'true',
            'pages': 'true',
            'categories': 'true',
            'suggestions': 'true',
            'queryCorrection': 'true',
            'suggestionsMaxResults': '3',
            'pageStartIndex': '0',
            'pagesMaxResults': '20',
            'categoryStartIndex': '0',
            'categoriesMaxResults': '20',
            'facets': 'true',
            'facetsShowUnavailableOptions': 'false',
            'recentlyViewedProducts': '',
            'ResultsTitleStrings': '2',
            'ResultsDescriptionStrings': '2',
            'page': '1',
            'union[price][min]': 'price_NOK',
            'shopify_currency': 'NOK',
            'prepareVariantOptions': 'true',
            'output': 'jsonp',
            'callback': f'jQuery36008546270804256082_{int(start_time)}',
            '_': f'{int(start_time)}',
        }
        response = requests.get('https://searchserverapi.com/getresults', params=params, headers=headers, timeout=10)
        data = json.loads(response.text[response.text.find('{'):response.text.rfind('}')+1])
        for item in data['items']:
            disc = Disc()
            disc.name = item['title']
            if self.search.lower() not in disc.name.lower(): # check false results
                continue
            disc.url = f'{self.url}{item["link"]}'
            disc.manufacturer = item['vendor']
            disc.price = '{:.2f} kr'.format(float(item['price']))
            disc.img = item['image_link']
            disc.store = self.name
            self.discs.append(disc)

        self.scraper_time = time.time() - start_time
        print(f'Latitude64 scraper: {self.scraper_time}')
