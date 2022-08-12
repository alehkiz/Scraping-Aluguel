import time
import requests
from data import House
from config import houses_file
import pickle
from bs4 import BeautifulSoup as BS
from scrap import Request
from datetime import timedelta, datetime
from tqdm import tqdm


request = Request()
# request.load()

for i, v in tqdm(request.houses.items()):
    lst_save_time = datetime.now()
    save_interval=1
    if request.houses[i].type == None:
        res = requests.get(i)
        if res.status_code == 200:
            time.sleep(3)
            soup = BS(res.text, 'html.parser')
            type = soup.find(class_ = 'price__title')
            if type != None:
                request.houses[i].type = type.text
            else:
                request.houses[i].type = 'Não informado'
        else:
            if res.status_code == 429:
                print('Aguardando 30 segundos')
                time.sleep(30)
            print(res.status_code)
    save_time = timedelta(minutes=save_interval)

    if datetime.now() > (lst_save_time + save_time):
        request.save_houses()
        # print(f'Houses salvas às {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}')
        lst_save_time = datetime.now()
request.save_houses()
