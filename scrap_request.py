from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup as BS
import time
import config
from data import House
from util_class import Scraper
from functools import reduce
from tqdm import tqdm

class Request(Scraper):
    def __init__(self) -> None:
        self.houses = self.load_houses()
        self.houses = self.houses if self.houses != None else {}
        self.links = self.load_links()
    def load(self, page_num:int = 0, limit_range:int=100):
        lst_save_time = datetime.now()
        save_time = timedelta(minutes=3)
        current_page = page_num
        current_url_page = config.url_base
        for i in tqdm(range(0, limit_range)):
            time.sleep(1)
            url = Request.change_query_string_on_url(config.url_base, {'pagina': current_page})
            try:
                res = requests.get(url)
            except Exception as e:
                print(f'Houve uma exceção na página {current_page}\n{e}')
            if res.status_code != 200:
                raise Exception(f'Ocorreu um erro no acesso: {res.status_code}, página: {url}')
            soup = BS(res.text, 'html.parser')
            result = soup.find(class_ = 'results-list')
            items = result.find_all(class_ = 'property-card__content-link')
            self.links.extend(['https://www.vivareal.com.br'+_.get('href') for _ in items])
            current_page += 1
            current_url_page = Request.change_query_string_on_url(current_url_page, {'pagina': current_page})
        self.save_links()
        print(f'Links salvos às {datetime.now().strftime("%d/%m/%y, %H:%M:%S")}, página: {current_page}')
    def get_info(self, url : str, save=True):
        time.sleep(2)
        # print(f'Iniciando a URL: {url}')5
        house = House()
        try:
            res =  requests.get(url)
        except Exception as e:
            print(f'Houve uma exceção na página {url}\n{e}')
        if res.status_code != 200:
                while True:
                    if res.status_code == 429:
                        print(f'Limite de acessos esgotado! Aguardando 2 minutos')
                        time.sleep(120)
                    else:
                        break
                    res = requests.get(url)

        soup = BS(res.text, 'html.parser')
        try:
            inactive = soup.find(class_='inactive-udp__alert')
            if inactive.text.strip() == 'Você está vendo esta página porque o imóvel que buscava foi alugado ou está indisponível.':
                house.code = 'INATIVO'
                print('Imóvel inativo')
        except Exception as e:
            ...
        if house.code != 'INATIVO':
            house.title = soup.find(class_ = 'title__title').text
            house.address = soup.find(class_= 'title__address').text
            feats = soup.find(class_= 'features')
            dic_feats = {_.get('title').lower():_.text.strip() for _ in feats.find_all() if _.get('title') != None}
            house.area = Request.get_int_from_string(dic_feats['área'])
            house.bedrooms = Request.get_int_from_string(dic_feats['quartos'])
            house.bathrooms = [Request.get_int_from_string(_) for _ in dic_feats['banheiros'].split('\n') if 'banheiro' in _]
            house.parking = Request.get_int_from_string(dic_feats['vagas'])
            amen = soup.find_all(class_='amenities__list')
            if not amen:
                house.amenities = []
            else:
                house.amenities = reduce(lambda x, y: x+y, [[_.get('title') for _ in x.find_all('li')] for x in amen])
            price_content = soup.find(class_='price-container')
            price_info = Request.get_int_from_string(price_content.find(class_='price__price-info').text)
            house.price['rent'] = price_info if price_info != None else ''
            price_list = price_content.find(class_='price__list')
            items_price = price_list.find_all('span')
            price_iterator = range(0, len(items_price)-1, 2)
            dic_price = {items_price[_].text:items_price[_+1].text for _ in price_iterator}
            house.price = dict(rent=house.price['rent'], **dic_price)

        self.houses[url] = house

        if save is True:
            self.save_houses()
        return house

    def get_batch(self, list_links = [], save_interval=3):
        start_time = time.time()
        if not list_links:
            list_links = self.links
        lst_save_time = datetime.now()
        save_time = timedelta(minutes=save_interval)
        if not isinstance(list_links, list):
            raise Exception(f'{list_links} incorreto')
        for link in tqdm(list_links):
            if link in self.houses.keys():
                if not self.houses[link].address is None:
                    continue
            self.get_info(link)
            if datetime.now() > (lst_save_time + save_time):
                self.save_houses()
                print(f'Houses salvas às {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}')
                lst_save_time = datetime.now()
        self.save_houses()
        print(f'Finalizando\nTempo total: {time.time() - start_time} segundos')
