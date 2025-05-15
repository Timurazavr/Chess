from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from bot.lexicon.lexicon import LEXICON
from bot.keyboards.pagination_kb import create_keyboard, create_keyboard_chess
from bot.databases.db_session import create_session
from bot.databases.users_tg import User_tg
from bot.databases.games_chess import GameChess
from game_logic.chess_logic import Chess


router = Router()
storage = MemoryStorage()


class FSMFillForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    fill_id_game = State()


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, bot: Bot):
    await message.delete()
    message_id = (
        await message.answer(
            LEXICON["start"],
            reply_markup=create_keyboard("online_data", "offline_data"),
        )
    ).message_id
    session = create_session()
    user = session.get(User_tg, message.from_user.id)
    if user:
        try:
            await bot.delete_message(message.chat.id, user.last_message_id)
        except Exception:
            pass
        user.last_message_id = message_id
    else:
        user = User_tg(id=message.from_user.id, last_message_id=message_id)
        session.add(user)
    session.commit()
    session.close()


@router.callback_query(F.data == "offline_data", StateFilter(default_state))
async def process_offline_press(callback: CallbackQuery):
    session = create_session()
    user = session.get(User_tg, callback.from_user.id)
    if user.session_id and not user.session.is_finished:
        chess = Chess(eval(user.session.board)[-1])
    else:
        chess = Chess()
        game = GameChess(
            white_id=callback.from_user.id,
            black_id=callback.from_user.id,
            board=str([chess.get_fen()]),
        )
        session.add(game)
        session.commit()
        user.session_id = game.id
        session.commit()
        session.close()
    await callback.message.edit_text(
        text=LEXICON["motion_" + chess.who_walking],
        reply_markup=create_keyboard_chess(chess.field),
    )


@router.callback_query(F.data == "online_data", StateFilter(default_state))
async def process_online_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["choice"],
        reply_markup=create_keyboard("join_random", "join_friend", "create", "exit"),
    )


@router.callback_query(
    lambda x: x.message.text.isdigit()
    and len(x.message.text) == 2
    and 0 <= int(x.message.text[0]) <= 7
    and 0 <= int(x.message.text[1]) <= 7,
    StateFilter(default_state),
)
async def process_konch_press(callback: CallbackQuery, bot: Bot):
    session = create_session()
    game = session.get(User_tg, callback.from_user.id).session
    chess = Chess(eval(game.board)[-1])
    y1, x1 = map(int, callback.message.text)
    y2, x2 = map(int, callback.data[-2:])
    result = chess.move(x1, y1, x2, y2)
    if not result:
        await callback.message.edit_text(
            text=LEXICON["motion_" + chess.who_walking],
            reply_markup=create_keyboard_chess(chess.field),
        )
        return
    chess.get_stat()
    game.board = str(eval(game.board)[-2:] + [chess.get_fen()])
    game.is_finished = True
    if chess.mate:
        txt = LEXICON["mate_" + chess.to_who]
    elif chess.stalemate:
        txt = LEXICON["stalemate_" + chess.to_who]
    elif chess.draw:
        txt = LEXICON["draw"]
    else:
        txt = LEXICON["motion_" + chess.who_walking]
        game.is_finished = False
    for user in game.users_tg:
        await bot.edit_message_text(
            chat_id=user.id,
            message_id=user.last_message_id,
            text=txt,
            reply_markup=create_keyboard_chess(chess.field),
        )
    session.commit()
    session.close()


@router.callback_query(F.data.startswith("field"), StateFilter(default_state))
async def process_konch_press(callback: CallbackQuery):
    session = create_session()
    user = session.get(User_tg, callback.from_user.id)
    chess = Chess(eval(user.session.board)[-1])
    session.close()
    y, x = map(int, callback.data[-2:])
    if (
        not (chess.mate or chess.stalemate or chess.draw)
        and chess.is_current_player_figure(x, y)
        and (
            (
                chess.who_walking == "white"
                and user.session.white_id == callback.from_user.id
            )
            or (
                chess.who_walking == "black"
                and user.session.black_id == callback.from_user.id
            )
        )
        and user.session.black_id != -1
    ):
        await callback.message.edit_text(
            text=callback.data[-2:],
            reply_markup=create_keyboard_chess(chess.field),
        )
    else:
        await callback.answer()


@router.callback_query(F.data == "join_random", StateFilter(default_state))
async def process_join_random_press(callback: CallbackQuery, bot: Bot):
    session = create_session()
    game = (
        session.query(GameChess)
        .filter(GameChess.black_id == -1, GameChess.is_finished == 0)
        .first()
    )
    if game is None:
        await callback.answer(LEXICON["no_free_game"], show_alert=True)
    else:
        chess = Chess(eval(game.board)[-1])
        await bot.edit_message_text(
            chat_id=game.users_tg[0].id,
            message_id=game.users_tg[0].last_message_id,
            text=LEXICON["motion_" + chess.who_walking],
            reply_markup=create_keyboard_chess(chess.field),
        )
        game.black_id = callback.from_user.id
        session.get(User_tg, callback.from_user.id).session_id = game.id
        session.commit()
        await callback.message.edit_text(
            text=LEXICON["motion_" + chess.who_walking],
            reply_markup=create_keyboard_chess(chess.field),
        )
    session.close()


@router.callback_query(F.data == "join_friend", StateFilter(default_state))
async def process_join_random_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON["enter_id_or_cancel"])
    await state.set_state(FSMFillForm.fill_id_game)


@router.message(Command("cancel"), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, bot: Bot, state: FSMContext):
    session = create_session()
    user = session.get(User_tg, message.from_user.id)
    await bot.edit_message_text(
        chat_id=user.id,
        message_id=user.last_message_id,
        text=LEXICON["choice"],
        reply_markup=create_keyboard("join_random", "join_friend", "create", "exit"),
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.callback_query(F.data == "create", StateFilter(default_state))
async def process_join_random_press(callback: CallbackQuery):
    session = create_session()
    user = session.get(User_tg, callback.from_user.id)
    chess = Chess()
    game = GameChess(white_id=callback.from_user.id, board=str([chess.get_fen()]))
    session.add(game)
    session.commit()
    user.session_id = game.id
    session.commit()
    await callback.message.edit_text(
        text=LEXICON["wait"].format(game.id),
        reply_markup=create_keyboard_chess(chess.field),
    )
    session.close()


@router.callback_query(F.data == "end_game_data", StateFilter(default_state))
async def process_end_game_press(callback: CallbackQuery, bot: Bot):
    session = create_session()
    game = session.get(User_tg, callback.from_user.id).session
    for user in game.users_tg:
        await bot.edit_message_text(
            chat_id=user.id,
            message_id=user.last_message_id,
            text=LEXICON["start"],
            reply_markup=create_keyboard("online_data", "offline_data"),
        )
        user.session_id = None
    game.is_finished = True
    session.commit()
    session.close()


@router.message(StateFilter(FSMFillForm.fill_id_game))
async def process_cancel_command_state(message: Message, bot: Bot, state: FSMContext):
    try:
        session = create_session()
        user = session.get(User_tg, message.from_user.id)
        text = message.text
        if text.isdigit():
            session = create_session()
            game = session.get(GameChess, int(text))
            if game:
                if game.black_id == -1 and game.is_finished == 0:
                    chess = Chess(eval(game.board)[-1])
                    await bot.edit_message_text(
                        chat_id=game.users_tg[0].id,
                        message_id=game.users_tg[0].last_message_id,
                        text=LEXICON["motion_" + chess.who_walking],
                        reply_markup=create_keyboard_chess(chess.field),
                    )
                    game.black_id = message.from_user.id
                    session.get(User_tg, message.from_user.id).session_id = game.id
                    session.commit()
                    await bot.edit_message_text(
                        chat_id=user.id,
                        message_id=user.last_message_id,
                        text=LEXICON["motion_" + chess.who_walking],
                        reply_markup=create_keyboard_chess(chess.field),
                    )
                    await state.clear()
                else:
                    await bot.edit_message_text(
                        chat_id=user.id,
                        message_id=user.last_message_id,
                        text=LEXICON["started"],
                    )
            else:
                await bot.edit_message_text(
                    chat_id=user.id,
                    message_id=user.last_message_id,
                    text=LEXICON["not_find"],
                )
        else:
            await bot.edit_message_text(
                chat_id=user.id,
                message_id=user.last_message_id,
                text=LEXICON["enter_id_or_cancel"],
            )
    except Exception:
        pass
    finally:
        await message.delete()


@router.callback_query(F.data == "exit", StateFilter(default_state))
async def process_end_game_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["start"],
        reply_markup=create_keyboard("online_data", "offline_data"),
    )
