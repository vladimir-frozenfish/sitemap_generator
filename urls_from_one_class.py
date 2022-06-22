"""
получение ссылок с одной (главной) страницы сайта
создается на основе класса url
"""

import requests

from urllib import parse


class Url:
    """класс Url"""
    def __init__(self, url, parent=None):
        self.url = url if url.endswith('/') else url + '/'
        self.parent = parent
        # self.links = self.get_links()
        self.links = set()

    def __str__(self):
        return self.url if self.parent is None else f'{self.parent} -> {self.url}'

    def __repr__(self):
        # return self.url if self.parent is None else f'{self.parent} -> {self.url}'
        return self.url

    def __len__(self):
        return len(self.links)

    def get_html_text(self):
        if self.url.startswith('mailto:') or self.url.startswith('tel:'):
            return ''
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        return response.text

    def get_link_from_tag(self, tag_a):
        """возвращает ссылку из html-кода <a .... href="..." ..> .... </a>"""
        index_href = tag_a.find('href')
        end_url = tag_a.find('"', index_href + 6)
        return tag_a[index_href + 6: end_url]

    def get_links(self):
        """возвращает множество (set) ссылок из html-текста и помещает
        в атрибут класса links - изначально это множетво пустое"""
        html_text = self.get_html_text()

        # links = set()
        start_find = 0

        while True:
            index_a_start = html_text.find('<a ', start_find)
            if index_a_start == -1:
                break
            index_a_end = html_text.find('</a>', start_find)

            # получение ссылки, очищенной от тэгов
            href = self.get_link_from_tag(html_text[index_a_start:index_a_end + 4])

            # если ссылка не равна главной, то
            # добавление ссылки во множество, если ссылка относительная или с параметрами, то соединяется с базовой
            # links.add(parse.urljoin(self.url, href))
            link = parse.urljoin(self.url, href)
            if link != self.url:
                self.links.add(link)

            start_find = index_a_end + 4

        return self.links

    def print_links(self):
        print(self.url)
        for link in self.links:
            print(link)


if __name__ == '__main__':
    '''
    url_yatube = Url('http://frozenfish.pythonanywhere.com/')
    url_yatube.get_links()
    url_yatube.print_links()
    '''

    '''
    url_yatube_1 = Url('http://frozenfish.pythonanywhere.com/?page=3')
    url_yatube_1.get_links()
    url_yatube_1.print_links()
    '''

    url_google = Url('https://www.kinopoisk.ru/')

    url_google.get_links()
    url_google.print_links()




