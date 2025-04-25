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


def create_keyboard_chess(field) -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[
            InlineKeyboardButton(
                text=" " if field[i // 8][i % 8] is None else str(field[i // 8][i % 8]),
                callback_data=str(i // 8) + str(i % 8),
            )
            for i in range(64)
        ],
        InlineKeyboardButton(
            text=LEXICON["end_game_btn"], callback_data="end_game_btn"
        ),
        width=8
    )
    return keyb.as_markup()
