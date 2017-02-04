# simple-mitm-proxy (docs WIP)

Implementation of simple MITM proxy, which will change content of the page

# EN

## Intro

This project is the part of the application process to [Ivelum](http://ivelum.com/) company. You can find original
description of the assignment [here](https://docs.google.com/document/d/1bua6MXG9rHyreSPVPEZBkk14WYHy31ia4Vb2rnrgvS0/edit)
(it's in russian). Let me do the translation of it in the next chapter.

## Requirements

Main purpose is to implement the simplest http-proxy-server. It should be able ro run locally on port of your choice and
show pages of [Habrahabr](https://habrahabr.ru/). The feature is that each page must be modified - after each word with
length of 6 characters the `™` signed should be inserted. Please, see the example below.

http://habrahabr.ru/company/yandex/blog/258673/

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают проблемы и особенности TLS. Я хочу
воспользоваться этой возможностью, чтобы поговорить об одной из них, а именно — о настройке ciphersiutes.


http://127.0.0.1:8232/company/yandex/blog/258673/

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают проблемы и особенности TLS.
Я хочу воспользоваться этой возможностью, чтобы поговорить об одной из них, а именно™ — о настройке ciphersiutes. 

Requirements:

* Python 3.x
* you're free to use any publicly available library
* less code is better, PEP8 is must
* if there's not enough information (requirements), then, please, rely on the common sense

If this task seems to be very easy for you, then you can add this:

* command line arguments (port; host; site, different from habrahabr.ru and so on)
* после старта локального сервера автоматически запускается браузер с открытой обработанной™ главной страницей
* after start of the local server, a web browser will automatically be run (with opened modified™ page)

# RU

## Интро

Этот проект выполнен в рамках моего трудоустройства в компанию [Ivelum](http://ivelum.com/). Оригинальное описание
задание на русском языке находится в [этом гуглодоке](https://docs.google.com/document/d/1bua6MXG9rHyreSPVPEZBkk14WYHy31ia4Vb2rnrgvS0/edit).
На случай, если материал по ссылке больше не доступен я продублировал все требования в следующем заголовке.

## Требования

Основная задача - реализовать простейший http-прокси-сервер, запускаемый локально (порт на ваше усмотрение), который
показывает содержимое страниц Хабра. С одним исключением: после  каждого слова из шести букв должен стоять значок «™».
Примерно так:

http://habrahabr.ru/company/yandex/blog/258673/

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают проблемы и особенности TLS. Я хочу
воспользоваться этой возможностью, чтобы поговорить об одной из них, а именно — о настройке ciphersiutes.


http://127.0.0.1:8232/company/yandex/blog/258673/

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают проблемы и особенности TLS.
Я хочу воспользоваться этой возможностью, чтобы поговорить об одной из них, а именно™ — о настройке ciphersiutes. 

Условия:

* Python 3.x
* можно использовать любые общедоступные библиотеки, которые сочтёте нужным
* чем меньше кода, тем лучше. PEP8 — обязательно
* в случае, если не хватает каких-то данных, следует опираться на здравый смысл


Если задача кажется слишком простой, можно добавить следующее:

* параметры командной строки (порт, хост, сайт, отличный от хабра и т.п.)
* после старта локального сервера автоматически запускается браузер с открытой 
обработанной™ главной страницей
