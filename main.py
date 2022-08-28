from scrap import Request, teste
from config import *
from data import *
from rich.console import Console
import time
import re
if __name__ == '__main__':
    console = Console()
    rq = Request()
    console.rule('[bold blue]Configurando')
    num_pages = console.input('Informe a quantidade de páginas que serão acessadas, [gray]se nenhum valor for informado serão considerado 50 páginas, limite de 400:\n')
    num_pages = ''.join(re.findall('\d', num_pages))
    num_pages = int(num_pages) if num_pages != '' else 50
    num_pages = num_pages if num_pages <= 400 else 400
    console.print(f'Atualizando os links, para as [blue underline]{num_pages} primeiras páginas')
    start_time = time.time()
    rq.load(0, num_pages)
    console.print(f'Links atualizados, tempo para carregar os links: [blue bold]{time.time() - start_time} segundos')
    console.rule('[bold blue]Carregando páginas')
    start_time_pages = time.time()
    rq.get_batch(rq.links)
    console.print(f'Ótimo, está tudo atualizado, o tempo para carregar as páginas foi de : [blue bold]{time.time() - start_time_pages} segundos')
    console.print(f'E o tempo total foi de: [blue bold]{time.time() - start_time} segundos')
    console.print('[bold blue]Saindo...')


