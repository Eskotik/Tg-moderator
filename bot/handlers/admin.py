import time

from aiogram import types
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter

from bot.loader import bot, dp
from bot.utils.helpers import parse_mute_duration


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=["ban"],
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
)
async def ban(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    admin_id = message.from_user.id
    await bot.kick_chat_member(chat_id=message.chat.id, user_id=replied_user)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=(
            f"[{message.reply_to_message.from_user.full_name}]"
            f"(tg://user?id={replied_user})"
            f" was banned by admin [{message.from_user.full_name}]"
            f"(tg://user?id={admin_id})"
        ),
        parse_mode=types.ParseMode.MARKDOWN,
    )

@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=["unban"],
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
)
async def unban(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    await bot.unban_chat_member(chat_id=message.chat.id, user_id=replied_user)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        chat_id=message.chat.id,
        text=(
            f"[{message.reply_to_message.from_user.full_name}]"
            f"(tg://user?id={replied_user}) was unbanned in the chat."
        ),
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands=["mute"],
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
)
async def mute(message: types.Message):
    args = message.text.split()
    till_date = args[1] if len(args) > 1 else "15m"
    ban_for = parse_mute_duration(till_date)

    replied_user = message.reply_to_message.from_user.id
    now_time = int(time.time())

    try:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=replied_user,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=now_time + ban_for,
        )
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(
            chat_id=message.chat.id,
            text=(
                f"[{message.reply_to_message.from_user.full_name}]"
                f"(tg://user?id={replied_user}) was muted for {till_date}"
            ),
            parse_mode=types.ParseMode.MARKDOWN,
        )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id, text=f"Failed to mute: {str(e)}"
        )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["unmute"],
)
async def un_mute_user(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=replied_user,
        permissions=types.ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
        ),
    )
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(
        text=(
            f"[{message.reply_to_message.from_user.full_name}]"
            f"(tg://user?id={replied_user}) can write in the chat now"
        ),
        chat_id=message.chat.id,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["pin"],
    commands_prefix="!",
)
async def pin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.pin_chat_message(message_id=msg_id, chat_id=message.chat.id)


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["unpin"],
)
async def unpin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    try:
        await bot.unpin_chat_message(chat_id=message.chat.id, message_id=msg_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.reply("Message unpinned successfully!")
    except Exception as e:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.send_message(
            chat_id=message.chat.id, text=f"Failed to unpin message: {str(e)}"
        )


@dp.message_handler(
    AdminFilter(is_chat_admin=True),
    IsReplyFilter(is_reply=True),
    commands_prefix="!",
    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP],
    commands=["del"],
)
async def delete_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
