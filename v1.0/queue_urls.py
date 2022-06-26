import time
from collections import deque

from sitemap_classes import Url, Timing, SaveToFile


def main():
    urls_deque = deque()        # очередь для добавления классов страниц
    links_set = set()           # множество ссылок для сравнения

    timing_one_page = Timing()  # класс таймера для замера обработки одной страницы
    timing_all_job = Timing()   # класс таймера для замера времени работы всего кода
    timing_all_job.limit_time = 300  # установка лимита работы главного цикла в сек

    timing_all_job.start()      # отсчет времени всей работы


    url_main = Url('https://crawler-test.com/')

    save_file = SaveToFile(url_main.domain)         # класс записи данных в файлы
    save_file.create_directory()                    # создание папки для записи файлов
    save_file.save_to_log(f'---------------------Построение карты сайта {url_main}\n'
                          f'---------------------Начало работы - {time.asctime()}')

    urls_deque.append(url_main)
    links_set.add(url_main.url)

    count = 0
    while count < len(urls_deque) and timing_all_job.is_limit():
        timing_one_page.start()                     # отсчет времени для обработки одной страницы

        current_url = urls_deque[count]
        print(f'Запрос на страницу {current_url.url}')
        save_file.save_to_log(f'Запрос на страницу {current_url.url}')

        """если текущий url родственен главному, то получаем все ссылки на текущей странице, 
        после они добавятся в пустой атрибут .links,
        если текущий url - сторонний, то список ссылок не получаем, он будет пуст?
        также если запрос на текущую ссылку ведет на редирект ссылки которая есть в словаре ссылок,
        то также список ссылок не получаем"""
        if current_url.domain == url_main.domain:
            """если запрос текущего класса url не ведет на редирект, то берем ссылки с этого Urla"""
            if not current_url.is_redirect():
                current_url.get_links()
            else:
                current_url.url = current_url.response.url          # тогда url равен urlu, который переходит на редирект
                """если запрос текущего класса url ведет на редирект и 
                конечный url не находится в словаре ссылок, 
                то берем ссылки от конечного Urla,
                а также редирект ведет на этот же сайт, а не на сторонний"""
                if (current_url.url not in links_set) and current_url.get_domain() == url_main.domain:
                    current_url.url = current_url.response.url
                    current_url.get_links()

        # проходим по всем ссылкам текущей страницы, если их нету в очереди добавляем как классы в очередь
        for link in current_url.links:
            if link not in links_set:
                urls_deque.append(Url(link, current_url))
                links_set.add(link)
        count += 1

        timing_one_page.end()               # конец времени для обработки одной страницы

        print(f'Обработано страниц - {count}, '
              f'Обработанная страница - {current_url}, '
              f'Потрачено времени - {timing_one_page.get_timing()} сек.')
        save_file.save_to_log(f'Обработано страниц - {count}, '
                              f'Обработанная страница - {current_url}, '
                              f'Потрачено времени - {timing_one_page.get_timing()} сек.')

    print(f'Всего ссылок - {len(urls_deque)}')

    count = 1
    for url in urls_deque:
        print(f'{count}: {url}')
        count += 1

    save_file.save_to_links(urls_deque)             # запись результатов в текстовый файл

    timing_all_job.end()                            # конец времени всей работы
    print(f'\nВремя выполнения работы: {timing_all_job.get_timing()} сек.')
    if not timing_all_job.is_limit():
        print(f'Истек лимит времени на работу программы - {timing_all_job.limit_time} сек.')
        save_file.save_to_log(f'---------------------Истек лимит времени на работу программы - {timing_all_job.limit_time} сек.')
    save_file.save_to_log(f'---------------------Обработка сайта {url_main.url} завершена {time.asctime()}.\n'
                          f'---------------------Время выполнения работы: {timing_all_job.get_timing()} сек.\n'
                          f'---------------------Всего найдено ссылок - {len(urls_deque)}')


if __name__ == '__main__':
    main()