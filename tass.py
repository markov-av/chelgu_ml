import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver


def create_news_section_array():
    response = requests.get('https://tass.ru/')
    soup = BeautifulSoup(response.content, 'html.parser')
    news_section = []
    for a in soup.find_all('a', href=True):
        url_split = a['href'].split('/')
        if (len(url_split) > 1) \
                and (len(url_split) <= 3) \
                and url_split[0] == '':
            news_section.append(url_split[1])

    with open("tass.txt", "w") as text_file:
        for section in set(news_section):
            if section:
                print(section, file=text_file)

    return news_section


class NewsParser:
    def __init__(self, news_site, timer=10):
        # add browser options
        options = webdriver.ChromeOptions()
        options.binary_location = '/usr/bin/google-chrome-stable'
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        chrome_driver_binary = '/home/boozzee/chromedriver'
        self.driver = webdriver.Chrome(
            chrome_driver_binary,
            chrome_options=options
        )
        self.driver.get(news_site)
        self.timer = timer

    def news_scroll_parsing(self, news_section):
        import time
        SCROLL_PAUSE_TIME = 0.5
        # Get scroll height
        with open(f"links/{news_section}.txt", "w") as text_file:
            try:
                last_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                for sec in range(0, self.timer * 2):
                    # Scroll down to bottom
                    self.driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )
                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)

                    # Calculate new scroll height
                    # and compare with last scroll height
                    new_height = self.driver.execute_script(
                        "return document.body.scrollHeight"
                    )
                    if new_height == last_height:
                        print('Done!')
                        break
                    last_height = new_height

                res = self.driver.execute_script(
                    'return document.documentElement.outerHTML'
                )
                soup = BeautifulSoup(res, 'html.parser')
                for a in soup.find_all('a', href=True):
                    if a['href'].split('/')[1] == news_section \
                            or len(a['href'].split('/')) == 3:
                        print(f"{a['href']}", file=text_file)

                self.driver.close()

            except Exception as e:
                print('news_scroll_parsing: ', e)
                res = self.driver.execute_script(
                    'return document.documentElement.outerHTML'
                )
                soup = BeautifulSoup(res, 'html.parser')
                for a in soup.find_all('a', href=True):
                    if a['href'].split('/')[1] == news_section:
                        print(f"{a['href']}", file=text_file)

                self.driver.close()


def get_news_section_array():
    with open(f"tass.txt", "r") as text_file:
        lst = text_file.readlines()
    return [i.rstrip('\n') for i in lst]


def start_browser(news_section, timer=50):
    news_site = f'https://tass.ru/{news_section}'
    print(news_section)
    tass_parser = NewsParser(news_site, timer=timer)
    tass_parser.news_scroll_parsing(news_section)


if __name__ == '__main__':
    news_section_array = get_news_section_array()
    for section in tqdm(news_section_array):
        try:
            start_browser(section)
        except Exception as e:
            print('__main__:', e)
