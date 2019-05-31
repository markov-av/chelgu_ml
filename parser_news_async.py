import sys
import requests
import random
import hashlib
import time
import logging
from tqdm import tqdm
import aiohttp
import asyncio
from bs4 import BeautifulSoup


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True


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


def article_lenta(content):
    news = str()
    # Получить текст новости с сайте lenta.ru
    soup = BeautifulSoup(content, 'html.parser')

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


def article_tass(content):
    news = str()
    # Получить текст новости с сайте tass.ru
    soup = BeautifulSoup(content, 'html.parser')

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


async def safe_news(url, text, path='test_results'):
    file_name = hashlib.sha256(str(url).encode('utf-8')).hexdigest()
    with open(f"{path}/{file_name}.txt", "w") as text_file:
        print(f"{url}", file=text_file)
        print(f"{text}", file=text_file)


async def fetch_html(url: str,
                     session: aiohttp.ClientSession,
                     **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    html = await resp.text()
    return html


async def parse(url: str, session: aiohttp.ClientSession, **kwargs) -> set:
    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        pass
    else:
        # await safe_news(url, article_lenta(html))
        if 'lenta.ru' in url:
            await safe_news(url, article_lenta(html))
        else:
            await safe_news(url, article_tass(html))

        logger.info(f"Is parse: {url}")


async def bulk_crawl_and_write(urls: asyncio.coroutine, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                parse(url=url, session=session)
                # write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = get_urls(['tass_links/tass_links.txt', 'lenta_links/lenta_links.txt'])
    asyncio.run(bulk_crawl_and_write(urls=urls))













