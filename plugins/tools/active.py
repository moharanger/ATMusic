from pyrogram import filters
from pyrogram.types import Message

from ATMusic import app
from ATMusic.misc import SUDOERS
from ATMusic.utils.database.memorydatabase import (get_active_chats,
                                                   get_active_video_chats)
from strings import get_command

# Commands
ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")


@app.on_message(filters.command(["active", "aktif"]) & SUDOERS)
async def _(c, message):
    ms = str(len(await get_active_chats()))
    vd = str(len(await get_active_video_chats()))
    await app.send_message(
        message.chat.id,
        f"📀 <b>Active Chats</b>\n\n๏» <b>Music :</b> <code>{ms}</code>\n๏» <b>Video :</b> <code>{vd}</code>",
    )


@app.on_message(filters.command(["activevc", "activevoice", "vc"]) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text(f"<b>Getting voice chats active ...</b>")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[<code>{x}</code>]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [<code>{x}</code>]\n"
        j += 1
    if not text:
        await mystic.edit_text(f"<b>No Active Chats on : {app.mention}.</b>")
    else:
        await mystic.edit_text(
            f"<b>List of Currently Active Voice Chats :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["activev", "activevideo", "vd"]) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text(f"<b>Getting Active Video Chats ...</b>")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private Group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[<code>{x}</code>]\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [<code>{x}</code>]\n"
        j += 1
    if not text:
        await mystic.edit_text(f"<b>No Active Video Chats on : {app.mention}.</b>")
    else:
        await mystic.edit_text(
            f"<b>List of Currently Active Video Chats :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command("link") & SUDOERS)
async def tai_ya(_, message):
    if len(message.command) < 2:
        return await message.reply("> Silahkan berikan id grup!!")
    ajg = message.text.split(None, 1)[1]
    mmk = await app.export_chat_invite_link(int(ajg))
    return await message.reply_text(mmk)


__MODULE__ = "Active"
__HELP__ = """<blockquote><b><u>Active Commands:</u>
/ac - Cʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴏɴ ʙᴏᴛ.
/activevoice - Cʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴀɴᴅ ᴠɪᴅᴇᴏ ᴄᴀʟʟs ᴏɴ ʙᴏᴛ.
/activevideo - Cʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄᴀʟʟs ᴏɴ ʙᴏᴛ.
/stats - Cʜᴇᴄᴋ Bᴏᴛs Sᴛᴀᴛs</b></blockquote>"""
