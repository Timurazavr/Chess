from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lexicon.lexicon import LEXICON


def create_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(
        *[
            InlineKeyboardButton(text=LEXICON.get(b, b), callback_data=b)
            for b in buttons
        ]
    )
    return keyboard.as_markup()


def create_keyboard_chess(field) -> InlineKeyboardMarkup:
    keyb: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyb.row(
        *[
            InlineKeyboardButton(
                text=(
                    " "
                    if field[i // 8][i % 8] is None
                    else LEXICON[field[i // 8][i % 8].color][
                        field[i // 8][i % 8].__class__.__name__
                    ]
                ),
                callback_data="field" + str(i // 8) + str(i % 8),
            )
            for i in range(64)
        ],
        InlineKeyboardButton(
            text=LEXICON["end_game_data"], callback_data="end_game_data"
        ),
        width=8
    )
    return keyb.as_markup()
