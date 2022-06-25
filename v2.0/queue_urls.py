import time
import multiprocessing
from collections import deque

from sitemap_classes import Url, Timing, SaveToFile


# URL_MAIN = Url('http://frozenfish.site')
URL_MAIN = Url('http://frozenfish.pythonanywhere.com')
# URL_MAIN = Url('https://crawler-test.com/')
locker = multiprocessing.Lock()
URLS_QUEUE = deque()                         # очередь для добавления классов страниц
links_set = set()                           # множество ссылок для сравнения
timing_one_page = Timing()                  # класс таймера для замера обработки одной страницы
timing_all_job = Timing()                   # класс таймера для замера времени работы всего кода
save_file = SaveToFile(URL_MAIN.domain)     # класс записи данных в файлы


def current_url_job(current_url):
    """работа с текущей страницей"""
    current_url = current_url
    timing_one_page.start()  # отсчет времени для обработки одной страницы

    print(f'Запрос на страницу {current_url.url}, {multiprocessing.current_process().name}')
    save_file.save_to_log(f'Запрос на страницу {current_url.url}')

    """если текущий url родственен главному, то получаем все ссылки на текущей странице, 
    после они добавятся в пустой атрибут .links,
    если текущий url - сторонний, то список ссылок не получаем, он будет пуст?
    также если запрос на текущую ссылку ведет на редирект ссылки которая есть в словаре ссылок,
    то также список ссылок не получаем"""
    if current_url.domain == URL_MAIN.domain:
        """если запрос текущего класса url не ведет на редирект, то берем ссылки с этого Urla"""
        if not current_url.is_redirect():
            current_url.get_links()
        else:
            current_url.url = current_url.response.url  # тогда url равен urlu, который переходит на редирект
            """если запрос текущего класса url ведет на редирект и 
            конечный url не находится в словаре ссылок, 
            то берем ссылки от конечного Urla,
            а также редирект ведет на этот же сайт, а не на сторонний"""
            if (current_url.url not in links_set) and current_url.get_domain() == URL_MAIN.domain:
                current_url.url = current_url.response.url
                current_url.get_links()

    # проходим по всем ссылкам текущей страницы, если их нету в очереди добавляем как классы в очередь
    for link in current_url.links:
        if link not in links_set:
            URLS_QUEUE.append(Url(link, current_url))
            links_set.add(link)

    timing_one_page.end()  # конец времени для обработки одной страницы

    # with locker:
    save_file.save_to_shelve(current_url)  # запись в БД current_url

    print(f'Обработанная страница - {current_url}, '
          f'Потрачено времени - {timing_one_page.get_timing()} сек.')
    save_file.save_to_log(f'Обработанная страница - {current_url}, '
                          f'Потрачено времени - {timing_one_page.get_timing()} сек.')


def main():
    timing_all_job.start()      # отсчет времени всей работы

    save_file.create_directory()                    # создание папки для записи файлов
    save_file.save_to_log(f'---------------------Построение карты сайта {URL_MAIN}\n'
                          f'---------------------Начало работы - {time.asctime()}')

    # URLS_QUEUE.put(URL_MAIN)                     # помещение в очередь начального Url
    current_url_job(URL_MAIN)
    links_set.add(URL_MAIN.url)

    while URLS_QUEUE:
        print('Работает главный цикл!')
        url_mp = URLS_QUEUE.popleft()
        current_url_job(url_mp)
        # mp1 = multiprocessing.Process(target=current_url_job, args=(url_mp, ), name='mp1')
        # mp1.start()
        # mp1.join()


        '''
        with multiprocessing.Pool(multiprocessing.cpu_count()*2) as mp:
            mp_list = list(URLS_QUEUE)
            URLS_QUEUE.clear()
            mp.map(current_url_job, mp_list)
            mp.close()
            mp.join()
        '''

    timing_all_job.end()            # конец времени всей работы
    print(f'\nВремя выполнения работы: {timing_all_job.get_timing()} сек. Найдено ссылок - {len(links_set)}')
    save_file.save_to_log(f'---------------------Обработка сайта {URL_MAIN.url} завершена {time.asctime()}.\n'
                          f'---------------------Найдено ссылок - {len(links_set)}'
                          f'---------------------Время выполнения работы: {timing_all_job.get_timing()} сек.\n')


if __name__ == '__main__':
    main()