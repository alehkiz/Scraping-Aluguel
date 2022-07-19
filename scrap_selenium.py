from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import time
from datetime import timedelta, datetime

import config



from data import House, links
from util_class import Scraper


class Selenium(Scraper):
    def __init__(self, headless=False):
        if headless:
            options = Options()
            options.headless = True
            self.driver = Firefox(options=options)
        else:
            self.driver = Firefox()
        self.driver.get(config.url_base)
        self.main_window = self.driver.current_window_handle
        self.houses = self.load_houses()
        self.links = self.load_links()
        if not Selenium._check_url(self.driver.current_url) is True:
            raise Exception('Houve um erro no acesso')
    # terminamos na pagina 33
    def load(self, page_num:int = 0, limit_range:int=100):
        lst_save_time = datetime.now()
        save_time = timedelta(minutes=3)
        current_page = page_num
        self.driver.implicitly_wait(4)
        for i in range(0, limit_range):
            time.sleep(5)
            try:
                result_content = self.driver.find_element(By.CLASS_NAME, 'results-list')
                items = result_content.find_elements(By.CLASS_NAME, 'property-card__content-link')
                self.links.extend([_.get_attribute('href') for _ in items])
                current_page += 1
                new_url = Selenium.change_query_string_on_url(self.driver.current_url, {'pagina': current_page})
                self.driver.get(new_url)
            except Exception as e:
                print(f'Página {current_page} houve um erro\n {e}')
            if datetime.now() > (lst_save_time + save_time):
                # _temp_links = self.load_links()
                self.save_links()
                print(f'Links salvos às {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}, pagina {current_page}')
                lst_save_time = datetime.now()
    def get_info(self, link : str, save = True):
        house = House()
        self.driver.get(link)
        time.sleep(1)
        house.url = self.driver.current_url
        house.title = self.driver.find_element(By.CLASS_NAME, 'title__title').text
        try:
            inactive = self.driver.find_element(By.CLASS_NAME, 'inactive-udp__alert')
            if inactive.text == 'Você está vendo esta página porque o imóvel que buscava foi alugado ou está indisponível. ':
                house.code = 'INATIVO'
        except Exception as e:
            ...        
        feats = self.driver.find_element(By.CLASS_NAME, 'features')
        feats = feats.find_elements(By.TAG_NAME, 'li')
        dic_feats = {_.get_attribute('title').lower():_.text for _ in feats}
        house.area = dic_feats['área'][0: dic_feats['área'].find('m')]
        house.bedrooms = Selenium.get_int_from_string(dic_feats['quartos'])
        house.bathrooms = [Selenium.get_int_from_string(_) for _ in dic_feats['banheiros'].split('\n') if 'banheiro' in _]
        house.parking = Selenium.get_int_from_string(dic_feats['vagas'])

        try:
            amen = self.driver.find_elements(By.CLASS_NAME, 'amenities__list')
            house.amenities = [x.get_attribute('title') for x in amen.find_elements(By.CSS_SELECTOR, '*') if x.tag_name == 'li']
        except Exception as e:
            house.amenities = []

        price_content = self.driver.find_element(By.CLASS_NAME, 'price-container')
        price_info = Selenium.get_int_from_string(price_content.find_element(By.CLASS_NAME, 'price__price-info').text)
        house.price['rent'] = price_info if price_info != None else ''
        price_list = price_content.find_element(By.CLASS_NAME, 'price__list')
        items_price = price_list.find_elements(By.TAG_NAME, 'span')
        price_iterator = range(0, len(items_price)-1, 2)
        dic_price = {items_price[_].text:items_price[_+1].text for _ in price_iterator}

        house.price = dict(rent=house.price['rent'], **dic_price)
        self.houses[self.driver.current_url] = house
        if save is True:
            self.save_houses([house])
        return house

    def get_batch(self, list_links = [], save_interval=3):
        start_time = time.time()
        if not list_links:
            list_links = links
        lst_save_time = datetime.now()
        save_time = timedelta(minutes=save_interval)
        # print(type(self.houses))
        if not isinstance(list_links, list):
            raise Exception(f'{list_links} incorreto')
        for link in list_links:
            if link in self.houses.keys():
                continue
            self.get_info(link)
            # self.houses.append(self.get_info(link))
            if datetime.now() > (lst_save_time + save_time):
                self.save_houses()
                print(f'Links salvos às {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}')
                lst_save_time = datetime.now()
        self.save_houses()
        print(f'Finalizando\nTempo total: {time.time() - start_time} segundos')