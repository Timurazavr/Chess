from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
)
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_keyb, create_krest_nol
from databases.database import add_user, chang_user, search_user
from services.services import table_priv

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message, bot: Bot):
    last_message_id = search_user(message.from_user.id)
    if last_message_id:
        chang_user(message.from_user.id, message.message_id)
        bot.delete_message(message.chat.id, last_message_id)
    else:
        add_user(message.from_user.id, message.message_id)
    await message.answer(
        LEXICON["start"], reply_markup=create_keyb("online", "offline")
    )


@router.callback_query(F.data == "offline")
async def process_offline_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON["motion_white"], reply_markup=create_krest_nol()
    )


@router.callback_query(F.data == "online")
async def process_offline_press(callback: CallbackQuery):
    await callback.answer("Пока недоступно")


@router.callback_query(F.data.in_("123456789"))
async def process_nazm_press(callback: CallbackQuery):
    sp, a = callback.message.reply_markup.inline_keyboard, int(callback.data) - 1
    if sp[a // 3][a % 3].text == "-":
        sp[a // 3][a % 3].text = (
            "⭕" if users_db[callback.from_user.id]["hod"] else "❌"
        )
        users_db[callback.from_user.id]["hod"] = not users_db[callback.from_user.id][
            "hod"
        ]
        win = table_priv(sp)
        if win is not None:
            if win == "Ничья!":
                users_db[callback.from_user.id]["hod"] = True
                await callback.message.edit_text(text=win)
            else:
                await callback.message.edit_text(text=LEXICON["win"] + " " + win)
        else:
            mark = InlineKeyboardMarkup(inline_keyboard=sp)
            await callback.message.edit_text(
                text=(
                    LEXICON["nol"]
                    if users_db[callback.from_user.id]["hod"]
                    else LEXICON["krs"]
                ),
                reply_markup=mark,
            )

    await callback.answer()


@router.callback_query(F.data == "konch")
async def process_konch_press(callback: CallbackQuery):
    users_db[callback.from_user.id]["hod"] = True
    await callback.message.edit_text(text=LEXICON["end"])
