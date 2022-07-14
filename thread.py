import threading
import time

from requests import head
from scrap import Scraper


sc = Scraper(headless=True)

links = sc.load_links()

dic_links = {_:False for _ in links}
_sc = {}
for i in range(0, 200, 10):
    print('Iniciando lote')
    _sc[i] = Scraper(headless=True)
    _sc[i].get_batch(links[i: i+5])
    print("Finalizado lote")

