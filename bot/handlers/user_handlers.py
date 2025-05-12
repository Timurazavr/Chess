from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from bot.lexicon.lexicon import LEXICON
from bot.keyboards.pagination_kb import create_keyboard, create_keyboard_chess
from bot.databases.database import (
    is_user_exists,
    get_user,
    add_user,
    chang_user,
    get_sess,
    chang_sess,
)
from game_logic.chess_logic import Chess

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    await message.delete()
    message_id = (
        await message.answer(
            LEXICON["start"],
            reply_markup=create_keyboard("online_data", "offline_data"),
        )
    ).message_id
    if is_user_exists(message.from_user.id):
        last_message_id = get_user(message.from_user.id)
        chang_user(message.from_user.id, message_id)
        await bot.delete_message(message.chat.id, last_message_id)
    else:
        add_user(message.from_user.id, message_id)


@router.callback_query(F.data == "offline_data")
async def process_offline_press(callback: CallbackQuery):
    if get_sess(callback.from_user.id):
        chess = Chess(get_sess(callback.from_user.id))
        if not (chess.mate or chess.stalemate or chess.draw):
            await callback.message.edit_text(
                text=LEXICON["motion_" + chess.who_walking],
                reply_markup=create_keyboard_chess(chess.field),
            )
            if chess.shah:
                callback.answer(LEXICON["shah_error"])
        else:
            txt = "None"
            if chess.mate:
                txt = LEXICON["mate_" + chess.to_who]
            elif chess.stalemate:
                txt = LEXICON["stalemate_" + chess.to_who]
            elif chess.draw:
                txt = LEXICON["draw"]
            await callback.message.edit_text(
                text=txt,
                reply_markup=create_keyboard_chess(chess.field),
            )
    else:
        chess = Chess()
        chang_sess(callback.from_user.id, '"' + chess.get_fen() + '"')
        await callback.message.edit_text(
            text=LEXICON["motion_" + chess.who_walking],
            reply_markup=create_keyboard_chess(chess.field),
        )


@router.callback_query(F.data == "online_data")
async def process_online_press(callback: CallbackQuery):
    await callback.answer("Пока недоступно", True)


@router.callback_query(
    lambda x: x.message.text.isdigit()
    and len(x.message.text) == 2
    and 0 <= int(x.message.text[0]) <= 7
    and 0 <= int(x.message.text[1]) <= 7
)
async def process_konch_press(callback: CallbackQuery):
    chess = Chess(get_sess(callback.from_user.id))
    y1, x1 = map(int, callback.message.text)
    y2, x2 = map(int, callback.data[-2:])
    result = chess.move(x1, y1, x2, y2)
    if result:
        chang_sess(callback.from_user.id, '"' + chess.get_fen() + '"')
    chess.get_stat()
    if not (chess.mate or chess.stalemate or chess.draw):
        await callback.message.edit_text(
            text=LEXICON["motion_" + chess.who_walking],
            reply_markup=create_keyboard_chess(chess.field),
        )
        if chess.shah:
            callback.answer(LEXICON["shah_error"])
    else:
        txt = "None"
        if chess.mate:
            txt = LEXICON["mate_" + chess.to_who]
        elif chess.stalemate:
            txt = LEXICON["stalemate_" + chess.to_who]
        elif chess.draw:
            txt = LEXICON["draw"]
        await callback.message.edit_text(
            text=txt,
            reply_markup=create_keyboard_chess(chess.field),
        )


@router.callback_query(F.data.startswith("field"))
async def process_konch_press(callback: CallbackQuery):
    chess = Chess(get_sess(callback.from_user.id))
    y, x = map(int, callback.data[-2:])
    if not (
        chess.mate or chess.stalemate or chess.draw
    ) and chess.is_current_player_figure(x, y):
        await callback.message.edit_text(
            text=callback.data[-2:],
            reply_markup=create_keyboard_chess(chess.field),
        )
    else:
        await callback.answer()


@router.callback_query(F.data == "end_game_data")
async def process_end_game_press(callback: CallbackQuery):
    chang_sess(callback.from_user.id, "NULL")
    await callback.message.edit_text(
        LEXICON["start"], reply_markup=create_keyboard("online_data", "offline_data")
    )
