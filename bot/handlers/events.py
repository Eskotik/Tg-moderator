import asyncio

from aiogram import types

from bot.loader import bot, dp
from bot.utils.helpers import delete_message_after_delay


@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    chat_id = message.chat.id
    user = message.new_chat_members[0]
    user_name = user.first_name
    user_id = user.id
    user_mention = f"[{user_name}](tg://user?id={user_id})"

    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    welcome_message = await bot.send_message(
        chat_id=chat_id,
        text=(
            f"I saw you in my dreams, {user_mention}. "
            "The Oracle predicted your arrival. Welcome to the Matrix of Truth."
        ),
        parse_mode=types.ParseMode.MARKDOWN,
    )

    asyncio.create_task(
        delete_message_after_delay(
            welcome_message.chat.id, welcome_message.message_id, 20
        )
    )


@dp.message_handler(content_types=["left_chat_member"])
async def leave_chat(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
