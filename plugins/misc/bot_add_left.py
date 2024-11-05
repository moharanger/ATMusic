from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS, LOG_GROUP_ID
from ATMusic import app
from ATMusic.utils.database import (add_gban_user, blacklist_chat,
                                    delete_served_chat, delete_served_user,
                                    get_assistant)


@app.on_message(filters.new_chat_members)
async def join_watcher(_, message):
    try:
        userbot = await get_assistant(message.chat.id)
        chat = message.chat
        for members in message.new_chat_members:
            if members.id == app.id:
                count = await app.get_chat_members_count(chat.id)
                username = (
                    message.chat.username if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
                )
                msg = (
                    f"**ᴍᴜsɪᴄ ʙᴏᴛ ᴀᴅᴅᴇᴅ ɪɴ ᴀ ɴᴇᴡ ɢʀᴏᴜᴘ #New_Group**\n\n"
                    f"**ᴄʜᴀᴛ ɴᴀᴍᴇ:** {message.chat.title}\n"
                    f"**ᴄʜᴀᴛ ɪᴅ:** {message.chat.id}\n"
                    f"**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ:** @{username}\n"
                    f"**ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀ ᴄᴏᴜɴᴛ:** {count}\n"
                    f"**ᴀᴅᴅᴇᴅ ʙʏ:** {message.from_user.mention}"
                )
                await app.send_message(
                    LOG_GROUP_ID,
                    text=msg,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"ᴀᴅᴅᴇᴅ ʙʏ",
                                    url=f"tg://openmessage?user_id={message.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
                await userbot.join_chat(f"{username}")
    except Exception as e:
        print(f"Error: {e}")


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == app.id:
            remove_by = message.from_user if message.from_user else message.sender_chat
            if message.sender_chat:
                if message.sender_chat.username is None:
                    user_link = f"{message.sender_chat.title}"
                else:
                    user_link = f"[{message.sender_chat.title}](https://t.me/{message.sender_chat.username}"
            else:
                user_link = f"[{message.from_user.first_name} {message.from_user.last_name or ''}](tg://user?id={message.from_user.id})"
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
            )
            chat_id = message.chat.id
            left = f"✫ <b><u>#Left_group</u></b> ✫\nᴄʜᴀᴛ ɴᴀᴍᴇ : {title}\nᴄʜᴀᴛ ɪᴅ : {chat_id}\n\nʀᴇᴍᴏᴠᴇᴅ ʙʏ : {user_link}"
            await blacklist_chat(chat_id)
            if remove_by.id not in BANNED_USERS:
                await add_gban_user(user.id)
                BANNED_USERS.add(user.id)
                await delete_served_user(remove_by.id)
            await app.send_message(LOG_GROUP_ID, text=left)
            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        print(f"Error: {e}")
