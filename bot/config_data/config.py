from bot.secret import API_TOKEN, ADMIN_IDS
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # id админов


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(tg_bot=TgBot(token=API_TOKEN, admin_ids=ADMIN_IDS))
