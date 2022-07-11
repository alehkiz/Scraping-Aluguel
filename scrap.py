import time
from urllib.parse import urlsplit
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from dataclasses import dataclass
import config
from re import findall

@dataclass
class House:
    type: str = None
    address:str = None
    url: str = None
    price:dict = None
    total_price: float = None
    area: float = None
    bedrooms:int = None
    bathrooms:int = None
    parking:int = None
    amenities: dict = None
    description: str = None
    transport: str = None
    publisher_name: str = None
    code:str = None
    title:str = None


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

        
            
    def load(self):
        house = House()
        result_content = self.driver.find_element(By.CLASS_NAME, 'results-list')
        items = result_content.find_elements(By.CLASS_NAME, 'property-card__content-link')
        for item in items:
            item.click()
            time.sleep(3)
            _new_window = self.driver.window_handles[-1]
            self.driver.switch_to.window(_new_window)
            house.url = self.driver.current_url
            house.title = self.driver.find_element(By.CLASS_NAME, 'title__title').text
            feats = self.driver.find_element(By.CLASS_NAME, 'features')
            feats = feats.find_elements(By.TAG_NAME, 'li')
            dic_feats = {_.get_attribute('title').lower():_.text for _ in feats}
            house.area = dic_feats['área'][0: dic_feats['área'].find('m')]
            house.bedrooms = Scraper.get_int_from_string(dic_feats['quartos'])
            house.bathrooms = [Scraper.get_int_from_string(_) for _ in dic_feats['banheiros'].split('\n') if 'banheiro' in _]
            house.parking = Scraper.get_int_from_string(dic_feats['vagas'])
            amen = self.driver.find_element(By.CLASS_NAME, 'js-more-amenities')
            amen_open = self.driver.find_element(By.CLASS_NAME, 'more-amenities')
            amen_open.click()
            amenities = amen.find_elements(By.TAG_NAME, 'li')
            house.amenities = [_.text for _ in amenities]
            amen_close = self.driver.find_element(By.CLASS_NAME, 'amenities__button-close')
            amen_close.click()
            price_content = self.driver.find_element(By.CLASS_NAME, 'price-container')
            house.price['rent'] = ''.join([Scraper.get_int_from_string(_.text) for _ in price_content.find_elements(By.CLASS_NAME, 'price__price-info')])
            price_list = price_content.find_element(By.CLASS_NAME, 'price__list')
            items_price = price_list.find_elements(By.TAG_NAME, 'span')
            price_iterator = range(0, len(items_price), 2)
            dic_price = {items_price[_].text:items[_+1].text for _ in price_iterator}

            house.price = dict(house.price['rent'], **dic_price)
            self.houses.append(house)
