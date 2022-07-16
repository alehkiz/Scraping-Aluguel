from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as BS
import time
import config
from data import House
from util_class import Scraper

class Request(Scraper):
    def __init__(self) -> None:
        self.houses = self.load_houses()
        self.links = self.load_links()
    def load(self, page_num:int = 0, limit_range:int=100):
        lst_save_time = datetime.now()
        save_time = timedelta(minutes=3)
        current_page = page_num
        for i in range(0, limit_range):
            url = Request.change_query_string_on_url(config.url_base, {'pagina': current_page})
            res = requests.get(url)
            if res.status_code != 200:
                raise Exception(f'Ocorreu um erro no acesso: {res.status_code}')
            soup = BS(res.text, 'html.parser')
            result = soup.find(class_ = 'results-list')
            items = result.find_all(class_ = 'property-card__content-link')
            self.links.extend([_.get('href')])
