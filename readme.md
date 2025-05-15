Chess - кросс-платформенный проект про шахматы, позволяющий играть людям как с сайта, так и с тг бота вместе.

Инструкция по установке на Linux ubuntu:

**Установка Python**

* `sudo apt install python3-pip`
* `apt install python3.10-venv`
* `sudo apt install htop`

**Установка проекта**

* `git clone https://github.com/Timurazavr/Chess`
* `cd Chess`
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip install --upgrade pip`
* `pip install -r requirements.txt`

**Подготовка к запуску**

* Заполните config.json для web-приложения
* Заполните bot/config_data/config.py для тг бота

****
**Запуск программы**

* `htop python3 __init__.py &`