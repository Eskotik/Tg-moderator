import logging
import time
from random import randint

from aiogram import types
from aiogram.dispatcher.filters import IsReplyFilter

from bot.loader import bot, dp


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=["me"]
)
async def welcome(message: types.Message):
    if message.from_user.username is None:
        await message.reply(
            f"Name - {message.from_user.full_name}\nID - {message.from_user.id}\n"
        )
    else:
        await message.reply(
            f"Name - {message.from_user.full_name}\n"
            f"ID - <code>{message.from_user.id}</code>\n"
            f"Username - @{message.from_user.username}\n"
        )


@dp.message_handler(
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["dont_click_me"],
)
async def mute_random(message: types.Message):
    now_time = int(time.time())
    replied_user_id = message.from_user.id
    replied_user = message.from_user.full_name
    random_m = randint(1, 10)
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=replied_user_id,
        permissions=types.ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
        ),
        until_date=now_time + 60 * random_m,
    )
    await bot.send_message(
        text=(
            f"[{replied_user}](tg://user?id={replied_user_id})"
            f" won mute for {random_m} minute(s)"
        ),
        chat_id=message.chat.id,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    IsReplyFilter(is_reply=True),
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["report"],
)
async def report_by_user(message: types.Message):
    msg_id = message.reply_to_message.message_id
    user_id = message.from_user.id
    admins_list = await message.chat.get_administrators()

    for admin in admins_list:
        try:
            keyboard = types.InlineKeyboardMarkup()
            if message.chat.username:
                url = f"https://t.me/{message.chat.username}/{msg_id}"
            else:
                url = f"https://t.me/c/{str(message.chat.id)[4:]}/{msg_id}"
            
            keyboard.add(
                types.InlineKeyboardButton(
                    text="Go to message",
                    url=url
                )
            )
            
            await bot.send_message(
                text=(
                    f"User: [{message.from_user.full_name}](tg://user?id={user_id})\n"
                    f"Report for the following message:"
                ),
                chat_id=admin.user.id,
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=keyboard,
            )
        except Exception as e:
            logging.debug(
                "Can't send report message to %s. Error: %s", admin.user.id, e
            )

    await message.delete()
    await message.reply("Report sent to admins!")
