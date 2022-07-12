import time
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from dataclasses import dataclass, field
from typing import Dict, List
import config
from re import findall
import pickle

@dataclass
class House:
    type: str = None
    address:str = None
    url: str = None
    price:Dict[str, int] = field(default_factory=dict)
    total_price: float = None
    area: float = None
    bedrooms:int = None
    bathrooms:int = None
    parking:int = None
    amenities: List[str] = field(default_factory=list)
    description: str = None
    transport: str = None
    publisher_name: str = None
    code:str = None
    title:str = None

links = list()

class Scraper(Firefox):
    def __init__(self):
        self.driver = Firefox()
        self.driver.get(config.url_base)
        self.main_window = self.driver.current_window_handle
        self.houses = []
        if not Scraper._check_url(self.driver.current_url) is True:
            raise Exception('Houve um erro no acesso')

    @staticmethod
    def _check_url(url = config.url_base):
        _splited_url_base = urlsplit(config.url_base)
        _splited_url = urlsplit(url)
        return _splited_url.netloc == _splited_url_base.netloc

    @staticmethod
    def get_int_from_string(string : str) -> int:
        """Receive a var `string` and return a int from text. If hasn't a integer return `None`

        Args:
            string (str): Text that will get integers

        Returns:
            int: if `string` has integers, else return `None`
        """        
        integers = findall(r'\d+', string)

        if not integers:
            return None
        return int(''.join(integers))
    @staticmethod
    def change_query_string_on_url(url : str, query_params: dict):
        """Add to a `url` the `query_params`

        Args:
            url (str): The new `url` with params
        """
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query = parse_qs(query_string)
        if 'pagina' in query.keys():
            query.pop('pagina')
        query = dict(**query, **query_params)
        query_encoded = urlencode(query, doseq=True)
        return urlunsplit((scheme, netloc, path, query_encoded, fragment))
    # terminamos na pagina 33
    def load(self):
        current_page = 1
        house = House()
        self.driver.implicitly_wait(4)
        for i in range(0, 100):
            time.sleep(10)
            result_content = self.driver.find_element(By.CLASS_NAME, 'results-list')
            items = result_content.find_elements(By.CLASS_NAME, 'property-card__content-link')
            links.extend([_.get_attribute('href') for _ in items])
            current_page += 1
            new_url = Scraper.change_query_string_on_url(self.driver.current_url, {'pagina': current_page})
            self.driver.get(new_url)
            
    def get_info(self, list_links = []):
        if not list_links:
            list_links = links

        for link in list_links:
            house = House()
            self.driver.get(link)
            time.sleep(3)
            _new_window = self.driver.window_handles[-1]
            self.driver.switch_to.window(_new_window)
            try:
                cookie_bt = self.driver.find_element(By.CLASS_NAME, 'cookie-notifier__cta')
                cookie_bt.click()
            except Exception as e:
                pass
            time.sleep(1)
            house.url = self.driver.current_url
            house.title = self.driver.find_element(By.CLASS_NAME, 'title__title').text
            feats = self.driver.find_element(By.CLASS_NAME, 'features')
            feats = feats.find_elements(By.TAG_NAME, 'li')
            dic_feats = {_.get_attribute('title').lower():_.text for _ in feats}
            house.area = dic_feats['área'][0: dic_feats['área'].find('m')]
            house.bedrooms = Scraper.get_int_from_string(dic_feats['quartos'])
            house.bathrooms = [Scraper.get_int_from_string(_) for _ in dic_feats['banheiros'].split('\n') if 'banheiro' in _]
            house.parking = Scraper.get_int_from_string(dic_feats['vagas'])
            try:
                amen = self.driver.find_element(By.CLASS_NAME, 'js-more-amenities')
                amen_open = self.driver.find_element(By.CLASS_NAME, 'more-amenities')
                amen_open.click()
                amenities = amen.find_elements(By.TAG_NAME, 'li')
                house.amenities = [_.text for _ in amenities]
            except Exception as e:
                house.amenities = []
                print('Facilidade não encontrada')
            amen_close = self.driver.find_element(By.CLASS_NAME, 'amenities__button-close')
            amen_close.click()
            price_content = self.driver.find_element(By.CLASS_NAME, 'price-container')
            price_info = Scraper.get_int_from_string(price_content.find_element(By.CLASS_NAME, 'price__price-info').text)
            house.price['rent'] = price_info if price_info != None else ''
            price_list = price_content.find_element(By.CLASS_NAME, 'price__list')
            items_price = price_list.find_elements(By.TAG_NAME, 'span')
            price_iterator = range(0, len(items_price)-1, 2)
            dic_price = {items_price[_].text:items_price[_+1].text for _ in price_iterator}

            house.price = dict(rent=house.price['rent'], **dic_price)
            self.houses.append(house)
            # self.driver.close()
            # self.driver.switch_to.window(self.driver.window_handles[0])

        # for item in items:
        #     item.click()
        #     

    def save_links(self, list_links):
        if not list_links:
            list_links = links
            print('Links está vazia')
        with open(config.links_file, 'wb') as f:
            pickle.dump(links, f)
    
    def load_links(self):
        with open(config.links_file, 'rb') as f:
            return pickle.load(f)