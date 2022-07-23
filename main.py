from scrap import Request
from config import *
from data import *
from rich.console import Console
import time

if __name__ == '__main__':
    console = Console()
    rq = Request()
    console.rule('[bold blue]Configurando')
    console.print('Atualizando os links, para as [blue underline]50 primeiras páginas')
    start_time = time.time()
    rq.load(0, 50)
    console.print(f'Links atualizados, tempo para carregar os links: [blue bold]{time.time() - start_time} segundos')
    console.rule('[bold blue]Carregando páginas')
    start_time_pages = time.time()
    rq.get_batch(rq.links)
    console.print(f'Ótimo, está tudo atualizado, o tempo para carregar as páginas foi de : [blue bold]{time.time() - start_time_pages} segundos')
    console.print(f'E o tempo total foi de: [blue bold]{time.time() - start_time} segundos')
    console.print('[bold blue]Saindo...')


