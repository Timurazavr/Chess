from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_keyb(*buttons: str) -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[
            InlineKeyboardButton(text=LEXICON.get(b, b), callback_data=b)
            for b in buttons
        ]
    )
    return keyb.as_markup()


def create_chess(field) -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[
            InlineKeyboardButton(
                text=" " if field[i][j] is None else str(field[i][j]),
                callback_data=str(i) + str(j),
            )
            for i in range(8)
            for j in range(8)
        ],
        InlineKeyboardButton(text="Закончить игру", callback_data="konch"),
        width=8
    )
    return keyb.as_markup()
