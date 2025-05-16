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

* Заполните config.json по образцу
* `sudo nano /lib/systemd/system/myService.service`
* Заполните myService.service по образцу
* `sudo chmod 644 /lib/systemd/system/myService.service`
* `sudo systemctl daemon-reload`
* `sudo systemctl enable myService`

****
**Запуск программы**

* `sudo systemd start meService `

**Образцы**

* config.json

{
"PATH_TO_CHESS_FOLDER": "/home/pashok/PycharmProjects/chess",
"PATH_TO_CHESS_FOLDER_WIN": "C:\\Users\\timur\\Desktop\\Codes\\Chess",
"port": 61488,
"SECRET_KEY": "some badass key",
"SECRET_TG_API_KEY": "api"
}

* myService.service

[Unit]
Description=My app
After=network.target

[Service]
Type=idle
Restart=on-failure
User=root
ExecStart=/bin/bash -c 'cd /home/ubuntu/project/ && source env/bin/activate && python3 __init__.py'

[Install]
WantedBy=multi-user.target