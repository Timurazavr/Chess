from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon import LEXICON_COMMANDS


async def set_main_menu(bot: Bot):
    main_menu = [
        BotCommand(command=k, description=v) for k, v in LEXICON_COMMANDS.items()
    ]
    await bot.set_my_commands(main_menu)
