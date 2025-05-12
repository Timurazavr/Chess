from aiogram import Bot, Dispatcher
import asyncio
import logging

from bot.config_data.config import Config, load_config
from bot.handlers import user_handlers, other_handlers
from bot.keyboards.main_menu import set_main_menu


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

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)

    dp.include_routers(user_handlers.router, other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
