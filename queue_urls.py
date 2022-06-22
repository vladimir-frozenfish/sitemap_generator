from collections import deque

from urls_from_one_class import Url


def main():
    url_main = Url('http://frozenfish.pythonanywhere.com/')
    urls_deque = deque()
    urls_deque.append(url_main)

    count = 0
    while count < len(urls_deque):
        current_url = urls_deque[count]
        # проходим по всем ссылкам текущей страницы, если их нету в очереди добавляем как классы в очередь
        for link in current_url.links:
            pass

    print(urls_deque)


if __name__ == '__main__':
    main()