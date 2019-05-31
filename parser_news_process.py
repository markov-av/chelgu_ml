import requests
import random
import hashlib
import time
import logging
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from bs4 import BeautifulSoup


logger = logging.basicConfig(filename="logs.log", level=logging.INFO)


def article_lenta(response):
    news = str()
    # Получить текст новости с сайте lenta.ru
    soup = BeautifulSoup(response.content, 'html.parser')

    # Получаем дату новости с сайта lenta.ru
    for a in soup.find_all('time', itemprop='datePublished'):
        news = f"{a['datetime']}"

    # Получем заголовок новости с сайта lenta.ru
    for a in soup.find_all("h1", itemprop='headline'):
        news = f"{news}||{a.contents[0]}"

    # Body news
    for a in soup.find_all("div", itemprop="articleBody"):
        for text in a.find_all('p'):
            news = f"{news}||{text.getText()}"
    return news


def article_tass(response):
    news = str()
    # Получить текст новости с сайте tass.ru
    soup = BeautifulSoup(response.content, 'html.parser')

    # Получаем дату новости с сайта tass.ru
    for a in soup.find_all('dateformat', mode='abs'):
        news = f"{a['time']}"

    # Получем заголовок новости с сайта tass.ru
    for a in soup.find_all("h1"):
        news = f"{news}||{a.contents[0]}"

    # Body news
    for a in soup.find_all("div", class_="text-content"):
        for text in a.find_all('p'):
            news = f"{news}||{text.getText()}"
    return news


def add_links(path):
    links = []
    with open(f"{path}", "r") as text_file:
        links.extend([i.rstrip('\n') for i in text_file.readlines()])
    return links


def get_urls(paths: list):
    links = []
    for path_links in paths:
        links.extend(add_links(path_links))
    yield from sorted(links, key=lambda k: random.random())


def safe_news(response: requests.Response, text,path='results'):
    file_name = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
    with open(f"{path}/{file_name}.txt", "w") as text_file:
        print(f"{response.url}", file=text_file)
        print(f"{text}", file=text_file)


def parse(url):
    r = requests.get(url)
    if 'lenta.ru' in r.url:
        safe_news(r, article_lenta(r))
    else:
        safe_news(r, article_tass(r))


if __name__ == '__main__':
    urls = get_urls(['tass_links/tass_links.txt', 'lenta_links/lenta_links.txt'])
    with ProcessPoolExecutor(max_workers=4) as executor:
        start = time.time()
        futures = [executor.submit(parse, url) for url in urls]
        results = []
        for result in tqdm(as_completed(futures)):
            results.append(result)
        end = time.time()
        print("Time Taken: {:.6f}s".format(end-start))

