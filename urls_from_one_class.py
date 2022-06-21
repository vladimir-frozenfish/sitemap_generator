"""
получение ссылок с одной (главной) страницы сайта
создается на основе класса url
"""

import requests


class Url:
    def __init__(self, url):
        self.url = url
        self.urls = self.get_urls()

    def __str__(self):
        return self.url

    def __len__(self):
        return len(self.urls)

    def get_html_text(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        return response.text

    def get_url_from_tag(self, tag_a):
        """возвращает ссылку из html-кода <a .... href="..." ..> .... </a>"""
        index_href = tag_a.find('href')
        end_url = tag_a.find('"', index_href + 6)
        return tag_a[index_href + 6: end_url]

    def get_urls(self):
        """возвращает множество (set) ссылок из html-текста"""
        html_text = self.get_html_text()

        urls = set()
        start_find = 0

        while True:
            index_a_start = html_text.find('<a ', start_find)
            if index_a_start == -1:
                break
            index_a_end = html_text.find('</a>', start_find)

            # получение ссылки, очищенной от тэгов
            href = self.get_url_from_tag(html_text[index_a_start:index_a_end + 4])

            # проверка ссылки на относительность
            if href.startswith('/'):
                urls.add(self.url.rstrip('/') + href)
            else:
                urls.add(href)

            start_find = index_a_end + 4

        return urls

    def print_urls(self):
        for url in self.urls:
            print(url)


if __name__ == '__main__':
    url_main = Url('http://google.com')
    print(url_main)
    print(url_main.urls)
    print(len(url_main))

    url_crawler = Url('https://crawler-test.com/')
    url_crawler.print_urls()
    print(len(url_crawler))