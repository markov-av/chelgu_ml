import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class LentaLinks:
    def __init__(self, days_periods=1, url='https://lenta.ru/news/'):
        self.days_periods = days_periods
        self.url = url
        self.date_create = datetime.now()

    def _parse_url(self, day):
        date_ago = self.date_create - timedelta(days=day)
        url_ending = f"{date_ago.year}"\
            f"/{date_ago.strftime('%m')}" \
            f"/{date_ago.strftime('%d')}/"
        return self.url + url_ending

    def _range_by_day(self):
        for day in range(1, self.days_periods + 1):
            yield requests.get(self._parse_url(day)).content

    def _get_url_contents(self) -> BeautifulSoup:
        for content in self._range_by_day():
            yield from BeautifulSoup(content,
                                     'html.parser').find_all('a', href=True)

    def get_link(self):
        for a in self._get_url_contents():
            if 'news' in a['href'].split('/') \
                    and 'https:' not in a['href'].split('/'):
                yield a['href']


if __name__ == '__main__':
    # Получим ссылки на новости за N дней
    links = LentaLinks(days_periods=150)
    with open(f"lenta_links/lenta_links.txt", "w") as text_file:
        for link in links.get_link():
            print(f"https://lenta.ru{link}", file=text_file)

