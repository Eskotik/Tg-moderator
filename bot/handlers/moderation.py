import asyncio
import datetime
import logging

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter

from bot.config import EXEMPT_CHANNEL_ID, WHITE_CHANNEL_ID
from bot.loader import bot, dp
from bot.utils.helpers import delete_message_after_delay

warnings: dict[int, int] = {}


async def handle_violation(message, username, user_id, violation_type):
    if user_id not in warnings:
        warnings[user_id] = 1
        warning_message = await message.reply(
            f"@{username}, <b><u>I cannot allow anyone else to be deceived by the Matrix🕶</u></b>. "
            f"Warning [{warnings[user_id]} of 3] for {violation_type}.",
            parse_mode="HTML",
        )
    else:
        warnings[user_id] += 1
        if warnings[user_id] <= 3:
            warning_message = await message.reply(
                f"@{username}, <b><u>I cannot allow anyone else to be deceived by the Matrix🕶</u></b>. "
                f"Warning [{warnings[user_id]} of 3] for {violation_type}.",
                parse_mode="HTML",
            )
        else:
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                until_date=datetime.datetime.now() + datetime.timedelta(minutes=1),
                can_send_messages=False,
            )
            await message.reply(
                f"@{username}, you have been muted for 5 hours for {violation_type}."
            )
            await bot.delete_message(message.chat.id, message.message_id)
            warnings[user_id] = 0
            return

    asyncio.create_task(
        delete_message_after_delay(
            warning_message.chat.id, warning_message.message_id, 10
        )
    )
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=["text", "photo", "video"])
async def handle_text_messages(message: types.Message):
    if message.text and (message.text.startswith("/") or message.text.startswith("!")):
        return

    if message.sender_chat and str(message.sender_chat.id) == EXEMPT_CHANNEL_ID:
        return

    if (
        message.forward_from_chat
        and str(message.forward_from_chat.id) == EXEMPT_CHANNEL_ID
    ):
        return

    is_admin = await AdminFilter(is_chat_admin=True).check(message)
    user_id = message.from_user.id
    username = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.first_name
    )

    logging.debug("Message: %s", message)

    if is_admin:
        return

    if "forward_from_chat" in message:
        if str(message.forward_from_chat.id) != WHITE_CHANNEL_ID:
            await handle_violation(
                message,
                message.from_user.username,
                message.from_user.id,
                "forwarding messages from other channels",
            )

    if message.forward_from:
        await handle_violation(
            message,
            message.from_user.username,
            message.from_user.id,
            "forwarding messages from other bots",
        )

    if message.entities:
        for entity in message.entities:
            if entity.type == "url":
                url = message.text[entity.offset : entity.offset + entity.length]
                if not url.startswith("https://www.tradingview.com/"):
                    await handle_violation(message, username, user_id, "links")
                    break
