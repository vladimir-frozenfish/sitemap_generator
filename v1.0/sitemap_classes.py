"""
получение ссылок с одной (главной) страницы сайта
создается на основе класса url
"""

import os
import requests
import time

from urllib import parse


class Url:
    """класс Url"""
    def __init__(self, url, parent=None):
        self.url = url if url.endswith('/') else url + '/'
        self.response = None
        self.parent = parent
        self.domain = self.get_domain()
        self.links = set()

    def __str__(self):
        return self.url if self.parent is None else f'{self.parent} -> {self.url}'

    def __repr__(self):
        return self.url

    def __len__(self):
        return len(self.links)

    def get_domain(self):
        """возвращает имя домена или None,
        если в ссылке домена нет (напрмер mailto:....)"""
        '''
        # возвращает имя домена без субдоменов
        subdomain = parse.urlparse(self.url).netloc.split('.')
        if subdomain == ['']:
            return None
        return '.'.join(subdomain[-2:])
        '''
        return parse.urlparse(self.url).netloc              # возвращает имя с субдоменами


    def get_response(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
        }
        try:
            self.response = requests.get(self.url, headers=headers, timeout=5)
            self. response.encoding = 'utf-8'
        except:
            self.response = 'error'

    def get_html_text(self):
        if self.url.startswith('mailto:') or self.url.startswith('tel:'):
            return ''
        if self.response is None:
            self.get_response()
        if self.response == 'error':
            return ''
        return self.response.text

    def is_redirect(self):
        """функция возвращает True, если Response, на изначальный Url дает редирект"""
        if self.response is None:
            self.get_response()
        if self.response == 'error':
            return False
        if self.response.history:
            return self.response.history[0].is_redirect
        return False

    def get_link_from_tag(self, tag_a):
        """возвращает ссылку из html-кода <a .... href="..." ..> .... </a>"""
        index_href = tag_a.find('href')
        end_url = tag_a.find('"', index_href + 6)
        return tag_a[index_href + 6: end_url]

    def get_links(self):
        """возвращает множество (set) ссылок из html-текста и помещает
        в атрибут класса links - изначально это множетво пустое"""
        html_text = self.get_html_text()

        if self.is_redirect():
            self.url = self.response.url

        start_find = 0
        while True:
            index_a_start = html_text.find('<a ', start_find)
            if index_a_start == -1:
                break
            index_a_end = html_text.find('</a>', start_find)
            if index_a_end == -1:
                break

            # получение ссылки, очищенной от тэгов
            href = self.get_link_from_tag(html_text[index_a_start:index_a_end + 4])

            # если ссылка не равна главной, то
            # добавление ссылки во множество, если ссылка относительная
            # или с параметрами, то соединяется с базовой
            link = parse.urljoin(self.url, href)
            # пробуем варинат занесения ссылок без параметров GET
            link = parse.urlparse(link)
            link_without_get = link.scheme + "://" + link.netloc + link.path
            if link_without_get != self.url:
                self.links.add(link_without_get)

            start_find = index_a_end + 4

        return self.links

    def print_links(self):
        print(self.url)
        for link in self.links:
            print(link)


class Timing:
    """класс замера времени выполнения кода
    для замера времени необходимо:
    создать класс,
    сделать начальную отметку - имя_объекта_класса.start(),
    сделать конечную отметку - имя_объекта_класса.end()
    получить время выполнения кода - имя_объекта_класса.get_timing()"""
    def __init__(self):
        self.time_start = float()
        self.time_end = float()
        self.limit_time = None

    def start(self):
        self.time_start = time.time()

    def end(self):
        self.time_end = time.time()

    def get_timing(self):
        return round(self.time_end - self.time_start, 4)

    def is_limit(self):
        """для установки лимита работы программы или цикла"""
        if self.limit_time is None or (time.time() - self.time_start) < self.limit_time:
            return True
        return False


class SaveToFile:
    def __init__(self, domain):
        self.directory = domain
        self.log_path = self.directory + '/logs.txt'
        self.links_path = self.directory + '/links.txt'

    def create_directory(self):
        """создание директории"""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save_to_log(self, data):
        with open(self.log_path, 'a', encoding='utf-8') as file:
            file.write(data + '\n')

    def save_to_links(self, queue):
        count = 1
        with open(self.links_path, 'w', encoding='utf-8') as file:
            for link in queue:
                file.write(f'{count}: {link}\n')
                count += 1


if __name__ == '__main__':
    pass