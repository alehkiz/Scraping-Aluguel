import config
from urllib.parse import urlsplit, urlunsplit, urlencode, parse_qs
from re import findall
import pickle
from os.path import isfile

class Scraper:

    links = []
    houses = {}
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


    def load_houses(self):
        return self.load_file(config.houses_file)
    
    def save_houses(self):
        _temp = self.houses
        self.houses = self.load_houses()
        self.houses = dict(self.houses, **_temp)
        self.save_file(config.houses_file, self.houses)

    def save_links(self):
        # _temp_links = self.load_links()
        # if not list_links:
        #     list_links = self.links
        #     print('Links está vazia')
        # _temp_links.extend(list_links)
        _temp_links = self.load_links()
        self.links = list(set(_temp_links+self.links))
        self.save_file(config.links_file, self.links)
    
    def load_links(self):
        return self.load_file(config.links_file)

    def load_file(self, file_path: str):
        if not isfile(file_path):
            return None
            raise FileNotFoundError(f'{file_path} não existe.')
        with open(file_path, 'rb') as f:
            try: 
                return pickle.load(f)
            except EOFError as e:
                EOFError('Arquivo vazio', e)
    
    def save_file(self, file_path:str, to_save):
        """Save a file with var to_save

        Args:
            file_path (str): Path of file
            to_save : Variable that will be saved in file
        """        
        with open(file_path, 'wb') as f:
            pickle.dump(to_save, f)