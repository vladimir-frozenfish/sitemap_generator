"""
получение ссылок с одной (главной) страницы сайта
создается на основе класса url
"""

import requests

from urllib import parse


class Url:
    """класс Url"""
    def __init__(self, url, parent=None):
        self.url = url
        self.parent = parent
        self.links = self.get_links()

    def __str__(self):
        return self.url if self.parent is None else f'{self.parent} -> {self.url}'

    def __repr__(self):
        return self.url if self.parent is None else f'{self.parent} -> {self.url}'

    def __len__(self):
        return len(self.links)

    # def __eq__(self, other):



    def get_html_text(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        return response.text

    def get_link_from_tag(self, tag_a):
        """возвращает ссылку из html-кода <a .... href="..." ..> .... </a>"""
        index_href = tag_a.find('href')
        end_url = tag_a.find('"', index_href + 6)
        return tag_a[index_href + 6: end_url]

    def get_links(self):
        """возвращает множество (set) ссылок из html-текста"""
        html_text = self.get_html_text()

        links = set()
        start_find = 0

        while True:
            index_a_start = html_text.find('<a ', start_find)
            if index_a_start == -1:
                break
            index_a_end = html_text.find('</a>', start_find)

            # получение ссылки, очищенной от тэгов
            href = self.get_link_from_tag(html_text[index_a_start:index_a_end + 4])

            # добавление ссылки во множество, если ссылка относительная или с параметрами, то соединяется с базовой
            links.add(parse.urljoin(self.url, href))

            start_find = index_a_end + 4

        return links

    def print_links(self):
        for link in self.links:
            print(link)


if __name__ == '__main__':
    url_yatube = Url('http://frozenfish.pythonanywhere.com/')
    print(url_yatube)
    url_yatube.print_links()


    print(url_yatube.url == 'http://frozenfish.pythonanywhere.com/')



    url_yatube_next = Url('http://frozenfish.pythonanywhere.com/group/russian/')
    url_yatube_next.print_links()



