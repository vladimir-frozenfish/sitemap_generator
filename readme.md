![banner](https://downloader.disk.yandex.ru/preview/e0810a4ccc78dd62d033cb221cb1bbc35124324b2a31e56b5d6a8fe9705b452c/62b86a11/9bHaeAu13xtInrOkwMzZ49YyErMHQQUE3J5cdpYQijo3-UlU7Su7cg_EAu57vp27DFbvDi1kxThvw1W0snPpyQ%3D%3D?uid=0&filename=banner.png&disposition=inline&hash=&limit=0&content_type=image%2Fpng&owner_uid=0&tknv=v2&size=2048x2048)
## Скрипт генерации карты сайта
### v1.0
#### Файлы:
- sitemap_classes.py - описание классов Url, Timing, SaveToFile
- queue_urls.py - выполнение скрипта

Скрипт v1.0 ищет ссылки на сайте. Условия:
- запрос на страницу осуществляется с помощью - request.get
- если ссылка на сторонний сайт - дальше не идет 
- если ссылка на субдомен - дальше не идет
- если редирект, то учитывает ссылку на которую идет редирект
- GET-запрос в ссылке отбрасывается
- устновлен лимит работы программы в 300 сек. (5 мин.). Лимит можно изменить в атрибуте timing_all_job.limit_time в queue_urls.py. Если лимит надо убрать, то необходимо закоментировать этот атрибут.

Для запуска скрипта необходимо:  
```
- в queue_urls.py в переменной url_main - внести адрес страницы в формате http://сайт.ру
- запустить скрипт - python queue_urls.py
```

Запись данных и логи:
- создается папка соответсвующая имени сайта - "сайт.ру"
- logs.txt - записываются логи
- links.txt - записываются найденные ссылки в формате Родительская ссылка -> ссылка
- при работе скрипта также логи выводятся в терминал
- по окончанию поиска ссылок - результат также выводится в терминал

### Результат работы скрипта на некторых сайтах:
| URL сайта | Время обработки | Кол-во ссылок |  
| --------- | --------------- | ------------- |
| google.com | 2 сек. | 34 |
| crawler-test.com | 384 сек. | 843 (http и https) |
| vk.com | 27 сек. | 64 |
| stackoverflow.com | 300 сек. (лимит) | 9550 |
| frozenfish.pythonanywhere.com | 18 сек. | 43 |

### Работа над сдедующей версией v2.0 - необходимо реализовать:
- запись в файл типа shelve объектов класса Url - done
- многопоточность
- диалоговое меню
- работа через командную строку






 