import time
from collections import deque

from sitemap_classes import Url, Timing, SaveToFile


def main():
    urls_deque = deque()        # очередь для добавления классов страниц
    links_set = set()           # множество ссылок для сравнения

    timing_one_page = Timing()  # класс таймера для замера обработки одной страницы
    timing_all_job = Timing()   # класс таймера для замера времени работы всего кода

    timing_all_job.start()      # отсчет времени всей работы

    # url_main = Url('https://yandex.ru')
    # url_main = Url('http://crawler-test.com/')
    # url_main = Url('https://github.com/')
    # url_main = Url('http://frozenfish.pythonanywhere.com')
    url_main = Url('http://frozenfish.site')
    # url_main = Url('https://www.google.com')
    # url_main = Url('https://stackoverflow.com/')

    save_file = SaveToFile(url_main.domain)         # класс записи данных в файлы
    save_file.create_directory()                    # создание папки для записи файлов
    save_file.save_to_log(f'---------------------Построение карты сайта {url_main}\n'
                          f'---------------------Начало работы - {time.asctime()}')

    urls_deque.append(url_main)
    links_set.add(url_main.url)

    count = 0
    while count < len(urls_deque):
        timing_one_page.start()                     # отсчет времени для обработки одной страницы

        current_url = urls_deque[count]

        """если текущий url родственен главному, то получаем все ссылки на текущей странице, 
        после они добавятся в пустой атрибут .links,
        если текущий url - сторонний, то список ссылок не получаем, он будет пуст"""
        if current_url.domain == url_main.domain:
            current_url.get_links()
        # проходим по всем ссылкам текущей страницы, если их нету в очереди добавляем как классы в очередь
        for link in current_url.links:
            if link not in links_set:
                urls_deque.append(Url(link, current_url))
                links_set.add(link)
        count += 1

        timing_one_page.end()               # конец времени для обработки одной страницы

        print(f'Обработано страниц - {count}, '
              f'Обратотанная страница - {current_url}, '
              f'Потрачено времени - {timing_one_page.get_timing()} сек.')
        save_file.save_to_log(f'Обработано страниц - {count}, '
              f'Обратотанная страница - {current_url}, '
              f'Потрачено времени - {timing_one_page.get_timing()} сек.')


    print(f'Всего ссылок - {len(urls_deque)}')

    count = 1
    for url in urls_deque:
        print(f'{count}: {url}')
        count += 1

    save_file.save_to_links(urls_deque)

    timing_all_job.end()            # конец времени всей работы
    print(f'\nВремя выполнения работы: {timing_all_job.get_timing()} сек.')
    save_file.save_to_log(f'---------------------Обработка сайта {url_main.url} завершена {time.asctime()}.\n'
                          f'---------------------Время выполнения работы: {timing_all_job.get_timing()} сек.\n'
                          f'---------------------Всего найдено ссылок - {len(urls_deque)}')


if __name__ == '__main__':
    main()