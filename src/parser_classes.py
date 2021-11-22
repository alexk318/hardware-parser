from abc import ABC, abstractmethod
import requests

import bs4
from bs4 import BeautifulSoup

from html_data import find_product_data_shop, find_product_data_forcecom, find_product_data_tomas


class Parser(ABC):
    def __init__(self, url):
        self.url = url

    @staticmethod
    def get_html(url, params=None):
        html = requests.get(url,
                            headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                                                   '(KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                                     'accept': '*/*'},

                            params=params)

        return html

    @abstractmethod
    def get_pages_count(self):
        pass

    @abstractmethod
    def get_data(self):
        pass


class ParserShop(Parser):
    def __init__(self, url):
        Parser.__init__(self, url)
        self.soup_pagination = BeautifulSoup(self.get_html(self.url).text, 'html.parser', parse_only=bs4.SoupStrainer(
            'div', {'class': 'bx-pagination-container row'}))

    def get_pages_count(self):
        pagination = self.soup_pagination.find('div', class_='bx-pagination-container row').find_all('li', class_='')
        pages_count = int(pagination[-1].get_text())

        return pages_count

    def get_data(self):
        data = []

        for page in range(1, self.get_pages_count() + 1):
            html = self.get_html(self.url, params={'PAGEN_1': page})
            soup = BeautifulSoup(html.text, 'html.parser',
                                 parse_only=bs4.SoupStrainer('div', {'class': 'bx_catalog_item double'}))

            items = soup.find_all('div', class_='bx_catalog_item double')

            for item in items:
                data.append(find_product_data_shop(item))

        return data


class ParserForcecom(Parser):
    def __init__(self, url):
        Parser.__init__(self, url)
        self.soup_pagination = BeautifulSoup(self.get_html(self.url).text, 'html.parser',
                                             parse_only=bs4.SoupStrainer('div', {
                                                 'class': 'nums'}))

    def get_pages_count(self):
        pagination = self.soup_pagination.find('div',
                                               class_='nums').find_all('a')
        pages_count = int(pagination[-1].get_text())

        return pages_count

    def get_data(self):
        data = []

        for page in range(1, self.get_pages_count() + 1):
            html = self.get_html(self.url, params={'PAGEN_1': page})

            soup = BeautifulSoup(html.text, 'html.parser',
                                 parse_only=bs4.SoupStrainer('div', {'class': 'list_item_wrapp item_wrap item'}))

            items = soup.find_all('div', class_='list_item_wrapp item_wrap item')

            for item in items:
                data.append(find_product_data_forcecom(item))

        return data


class ParserTomas(Parser):
    def __init__(self, url):
        Parser.__init__(self, url)
        self.soup_pagination = BeautifulSoup(self.get_html(self.url).text, 'html.parser',
                                             parse_only=bs4.SoupStrainer('div', {
                                                 'class': 'pager pager_goods'}))

    def get_pages_count(self):
        pagination = self.soup_pagination.find('div', class_='pager pager_goods').find_all('a')
        pages_count = int(pagination[-1].get_text())

        return pages_count

    def get_data(self):
        data = []

        for page in range(1, 2):
            html = self.get_html(self.url + str(page))
            soup = BeautifulSoup(html.text, 'html.parser', parse_only=bs4.SoupStrainer('div', {'class': 'goods__item'}))

            items = soup.find_all('div', class_='goods__item')

            for item in items:
                data.append(find_product_data_tomas(item))

        return data
