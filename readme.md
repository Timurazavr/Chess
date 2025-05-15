Chess - кросс-платформенный проект про шахматы, позволяющий играть людям как с сайта, так и с тг бота вместе.

Инструкция по установке на Linux ubuntu:

**Установка Python**

* `sudo apt install python3-pip`
* `apt install python3.10-venv`

**Установка проекта**

* `git clone https://github.com/Timurazavr/Chess`
* `cd Chess`
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip install supervisor`
* `pip install --upgrade pip`
* `pip install -r requirements.txt`

**Подготовка к запуску**
* Измените параметр в supervisord.conf directory на путь к приложению
* Перенесите файл supervisord.conf в папку /etc/supervisor/
* Заполните config.json для web-приложения
* Заполните bot/config_data/config.py для тг бота

****
**Запуск программы**

* `supervisord -c /etc/supervisor/supervisord.conf`

Не подробная но лаконичная информация о supervisor на сайте https://codex.so/supervisor