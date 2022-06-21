"""
получение ссылок с одной (главной) страницы сайта
"""

import requests


def get_url_from_tag(tag_a):
    """
    возвращает ссылку из html-кода <a .... href="..." ..> .... </a>
    """
    index_href = tag_a.find('href')
    end_url = tag_a.find('"', index_href + 6)

    return tag_a[index_href + 6: end_url]


def get_urls(html_text):
    """
    возвращает множество (set) ссылок из html-текста
    """
    print(html_text.count('<a '))
    print(html_text.count('</a>'))

    urls = set()
    start_find = 0

    while True:
        index_a_start = html_text.find('<a ', start_find)
        if index_a_start == -1:
            break
        index_a_end = html_text.find('</a>', start_find)

        urls.add(get_url_from_tag(html_text[index_a_start:index_a_end + 4]))

        start_find = index_a_end + 4

    return urls

# url = 'http://frozenfish.site'
url = 'http://crawler-test.com/'

response = requests.get(url)
response.encoding = 'utf-8'

urls = get_urls(response.text)
for one in urls:
    if one.startswith('/'):
        print(url.rstrip('/') + one)
    else:
        print(one)