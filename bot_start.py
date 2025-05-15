import json
import sys

from aiogram import Bot, Dispatcher
from os.path import join
import asyncio
import logging

from bot.config_data.config import Config, load_config
from bot.handlers import handlers
from bot.keyboards.main_menu import set_main_menu

from database.db_session import global_init


CONFIG = json.load(open("config.json", "r"))
if sys.platform.startswith("win"):
    PATH_TO_DB_FOLDER = CONFIG["PATH_TO_CHESS_FOLDER_WIN"]
else:
    PATH_TO_DB_FOLDER = CONFIG["PATH_TO_CHESS_FOLDER"]


# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    global_init(join(PATH_TO_DB_FOLDER, "database", "data.db"))
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)

    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
