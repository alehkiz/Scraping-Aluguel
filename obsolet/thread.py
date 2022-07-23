import threading
import time
import datetime

from requests import head
from scrap_selenium import Selenium
from scrap_request import Request

from data import House, links

scraper = Request()

links = scraper.load_links()

# links_values = 


def func(links):
    scraper.get_batch(links)
    print(f'Finalizado func às {datetime.datetime.now()}')

start_time = time.time()    
threads = [] 

number_of_threads = 2

barrier = threading.Barrier(number_of_threads)

for i in range(0, 3000, 20): # each thread could be like a new 'click' 
    th = threading.Thread(target=func, args=(links[i: i+20],))
    th.start() # could `time.sleep` between 'clicks' to see whats'up without headless option
    threads.append(th)        
for th in threads:
    th.join() # Main thread wait for threads finish
print("multiple threads took ", (time.time() - start_time), " seconds")





# sc = Selenium()

# links = sc.load_links()

# dic_links = {_:False for _ in links}
# # _sc = {}
# # for i in range(0, 200, 10):
# #     print('Iniciando lote')
# #     _sc[i] = Scraper(headless=True)
# #     _sc[i].get_batch(links[i: i+5])
# #     print("Finalizado lote")

# #threads

# def func(barrier, links):
#     _sc = Selenium()
#     _sc.get_batch(links)
#     _sc.driver.close()
#     print('wait for others')
#     # barrier.wait()

# start_time = time.time()    
# threads = [] 

# number_of_threads = 2

# barrier = threading.Barrier(number_of_threads)

# for i in range(0, 20, 5): # each thread could be like a new 'click' 
#     th = threading.Thread(target=func, args=(barrier, links[i: i+5]))
#     th.start() # could `time.sleep` between 'clicks' to see whats'up without headless option
#     threads.append(th)        
# for th in threads:
#     th.join() # Main thread wait for threads finish
# print("multiple threads took ", (time.time() - start_time), " seconds")