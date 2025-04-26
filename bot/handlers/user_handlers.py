from aiogram import F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_keyb, create_keyboard_chess
from databases.database import is_user_exists, get_user, add_user, chang_user
from services.services import session_dict, Chess

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    await message.delete()
    message_id = (
        await message.answer(
            LEXICON["start"], reply_markup=create_keyb("online_data", "offline_data")
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
    if callback.from_user.id not in session_dict:
        session_dict[callback.from_user.id] = Chess()
    await callback.message.edit_text(
        text=LEXICON["motion_" + session_dict[callback.from_user.id].who_walking],
        reply_markup=create_keyboard_chess(session_dict[callback.from_user.id].field),
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
    y1, x1 = map(int, callback.message.text)
    y2, x2 = map(int, callback.data[-2:])
    session_dict[callback.from_user.id].move(x1, y1, x2, y2)
    if session_dict[callback.from_user.id].is_finished is None:
        await callback.message.edit_text(
            text=LEXICON["motion_" + session_dict[callback.from_user.id].who_walking],
            reply_markup=create_keyboard_chess(
                session_dict[callback.from_user.id].field
            ),
        )
    else:
        await callback.message.edit_text(
            text=LEXICON["finish_" + session_dict[callback.from_user.id].is_finished],
            reply_markup=create_keyboard_chess(
                session_dict[callback.from_user.id].field
            ),
        )


@router.callback_query(F.data.startswith("field"))
async def process_konch_press(callback: CallbackQuery):
    y, x = map(int, callback.data[-2:])
    if session_dict[callback.from_user.id].is_finished is None and session_dict[
        callback.from_user.id
    ].is_figure(x, y):
        await callback.message.edit_text(
            text=callback.data[-2:],
            reply_markup=create_keyboard_chess(
                session_dict[callback.from_user.id].field
            ),
        )
    else:
        await callback.answer()


@router.callback_query(F.data == "end_game_data")
async def process_end_game_press(callback: CallbackQuery):
    del session_dict[callback.from_user.id]
    await callback.message.edit_text(
        LEXICON["start"], reply_markup=create_keyb("online_data", "offline_data")
    )
