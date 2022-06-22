from collections import deque

from urls_from_one_class import Url


def main():
    urls_deque = deque()    # очередь для добавления классов страниц
    links_set = set()       # множество ссылок для сравнения

    url_main = Url('https://thecode.media')
    # url_main = Url('http://crawler-test.com/')
    # url_main = Url('https://github.com/')
    # url_main = Url('http://frozenfish.pythonanywhere.com')
    # url_main = Url('http://frozenfish.site')

    urls_deque.append(url_main)
    links_set.add(url_main.url)

    count = 0
    while count < len(urls_deque):
        # print(urls_deque)
        current_url = urls_deque[count]

        """если текущий url родственен главному, то получаем все ссылки на текущей странице, 
        после они добавятся в пустой атрибут .links,
        если текущий url - сторонний, то список ссылок не получаем, он будет пуст"""
        if current_url.url.startswith(url_main.url):
            current_url.get_links()
        # проходим по всем ссылкам текущей страницы, если их нету в очереди добавляем как классы в очередь
        for link in current_url.links:
            if link not in links_set:
                urls_deque.append(Url(link, current_url))
                links_set.add(link)

        count += 1
        print(f'Обработано страниц - {count}, Обратотанная страницы - {current_url.url}')

    # print(len(urls_deque))
    # print(urls_deque)
    print(f'Всего ссылок - {len(urls_deque)}')
    # print(links_set)

    count = 1
    for url in urls_deque:
        print(f'{count}: {url}')
        count += 1

if __name__ == '__main__':
    main()