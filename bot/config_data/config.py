from dataclasses import dataclass
import json

CONFIG = json.load(open("config.json", "r"))
API_TOKEN = CONFIG["SECRET_TG_API_KEY"]


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # id админов


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(tg_bot=TgBot(token=API_TOKEN, admin_ids=[]))
