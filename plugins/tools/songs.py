import os
from asyncio import get_event_loop
from functools import partial

import wget
from pyrogram import filters
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL

from config import BANNED_USERS
from ATMusic import app
from ATMusic.utils.decorators.language import language
from strings import get_command

# Command
mycookies = "kn.txt"
# song
SONG_COMMAND = get_command("SONG_COMMAND")


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


@app.on_message(filters.command(["song"]) & ~BANNED_USERS)
@language
async def _(client, message, _):
    if len(message.command) < 2:
        return await message.reply(
            "❌ <b>Audio tidak ditemukan,</b>\Mohon masukan judul lagu dengan benar.",
        )
    infomsg = await message.reply("`Processing...`")
    try:
        search = (
            SearchVideos(
                str(message.text.split(None, 1)[1]),
                offset=1,
                mode="dict",
                max_results=1,
            )
            .result()
            .get("search_result")
        )
        link = f"https://youtu.be/{search[0]['id']}"
    except Exception as error:
        return await infomsg.edit(f"🔍 Pencarian...\n\n❌ Error: {error}")
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": mycookies,
        }
    )
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    except Exception as error:
        return await infomsg.edit(f"`Error: {error}`")
    thumbnail = wget.download(thumbs)
    await client.send_audio(
        message.chat.id,
        audio=file_path,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        caption=f"<b>Upload By: {app.me.mention}.</b>",
    )
    await infomsg.delete()
    for files in (thumbnail, file_path):
        if files and os.path.exists(files):
            os.remove(files)


@app.on_message(filters.command(["vsong", "video"]) & ~BANNED_USERS)
@language
async def _(client, message, _):
    if len(message.command) < 2:
        return await message.reply(
            "❌ <b>Video tidak ditemukan,</b>\nMohon masukan judul video dengan benar.",
        )
    infomsg = await message.reply("`Processing...`")
    try:
        search = (
            SearchVideos(
                str(message.text.split(None, 1)[1]),
                offset=1,
                mode="dict",
                max_results=1,
            )
            .result()
            .get("search_result")
        )
        link = f"https://youtu.be/{search[0]['id']}"
    except Exception as error:
        return await infomsg.edit(f"🔍 Pencarian...\n\n❌ Error: {error}")
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": mycookies,
        }
    )
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    except Exception as error:
        return await infomsg.edit(f"`Error: {error}`")
    thumbnail = wget.download(thumbs)
    await client.send_video(
        message.chat.id,
        video=file_path,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=f"<b>Upload by {app.me.mention}.</b>",
    )
    await infomsg.delete()
    for files in (thumbnail, file_path):
        if files and os.path.exists(files):
            os.remove(files)


"""
@app.on_message(filters.command(SONG_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def song_commad_group(client, message: Message, _):

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["SG_B_1"],
                    url=f"https://t.me/{app.username}?start=song",
                ),
            ]
        ]
    )

    await message.reply_text(_["song_1"], reply_markup=upl)


# Song Module


@app.on_message(filters.command(SONG_COMMAND) & filters.private & ~BANNED_USERS)
@language
async def song_commad_private(client, message: Message, _):

    await message.delete()

    url = await YouTube.url(message)

    if url:

        if not await YouTube.exists(url):

            return await message.reply_text(_["song_5"])

        mystic = await message.reply_text(_["play_1"])

        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)

        if str(duration_min) == "None":

            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:

            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )

        buttons = song_markup(_, vidid)

        await mystic.delete()

        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    else:

        if len(message.command) < 2:

            return await message.reply_text(_["song_2"])

    mystic = await message.reply_text(_["play_1"])

    query = message.text.split(None, 1)[1]

    try:

        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)

    except:

        return await mystic.edit_text(_["play_3"])

    if str(duration_min) == "None":

        return await mystic.edit_text(_["song_3"])

    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:

        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )

    buttons = song_markup(_, vidid)

    await mystic.delete()

    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(pattern=r"song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, CallbackQuery, _):

    callback_data = CallbackQuery.data.strip()

    callback_request = callback_data.split(None, 1)[1]

    stype, vidid = callback_request.split("|")

    buttons = song_markup(_, vidid)

    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, CallbackQuery, _):

    callback_data = CallbackQuery.data.strip()

    callback_request = callback_data.split(None, 1)[1]

    stype, vidid = callback_request.split("|")

    try:

        await CallbackQuery.answer(_["song_6"], show_alert=True)

    except:

        pass

    if stype == "audio":

        try:

            formats_available, link = await YouTube.formats(vidid, True)

        except:

            return await CallbackQuery.edit_message_text(_["song_7"])

        keyboard = InlineKeyboard()

        done = []

        for x in formats_available:

            check = x["format"]

            if "audio" in check:

                if x["filesize"] is None:

                    continue

                form = x["format_note"].title()

                if form not in done:

                    done.append(form)

                else:

                    continue

                sz = convert_bytes(x["filesize"])

                fom = x["format_id"]

                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{form} Quality Audio = {sz}",
                        callback_data=f"song_download {stype}|{fom}|{vidid}",
                    ),
                )

        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
        )

        return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)

    else:

        try:

            formats_available, link = await YouTube.formats(vidid, True)

        except Exception as e:

            print(e)

            return await CallbackQuery.edit_message_text(_["song_7"])

        keyboard = InlineKeyboard()

        # AVC Formats Only [ Alexa MUSIC BOT ]

        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]

        for x in formats_available:

            check = x["format"]

            if x["filesize"] is None:

                continue

            if int(x["format_id"]) not in done:

                continue

            sz = convert_bytes(x["filesize"])

            ap = check.split("-")[1]

            to = f"{ap} = {sz}"

            keyboard.row(
                InlineKeyboardButton(
                    text=to,
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            )

        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
        )

        return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


# Downloading Songs Here


@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, CallbackQuery, _):

    try:

        await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")

    except:

        pass

    callback_data = CallbackQuery.data.strip()

    callback_request = callback_data.split(None, 1)[1]

    stype, format_id, vidid = callback_request.split("|")

    mystic = await CallbackQuery.edit_message_text(_["song_8"])

    yturl = f"https://www.youtube.com/watch?v={vidid}"

    with yt_dlp.YoutubeDL({"quiet": True, "cookiefile": mycookies}) as ytdl:

        x = ytdl.extract_info(yturl, download=False)

    title = (x["title"]).title()

    title = re.sub("\W+", " ", title)

    thumb_image_path = await CallbackQuery.message.download()

    duration = x["duration"]

    if stype == "video":

        thumb_image_path = await CallbackQuery.message.download()

        width = CallbackQuery.message.photo.width

        height = CallbackQuery.message.photo.height

        try:

            file_path = await YouTube.download(
                yturl,
                mystic,
                songvideo=True,
                format_id=format_id,
                title=title,
            )

        except Exception as e:

            return await mystic.edit_text(_["song_9"].format(e))

        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )

        await mystic.edit_text(_["song_11"])

        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )

        try:

            await CallbackQuery.edit_message_media(media=med)

        except Exception as e:

            print(e)

            return await mystic.edit_text(_["song_10"])

        os.remove(file_path)

    elif stype == "audio":

        try:

            filename = await YouTube.download(
                yturl,
                mystic,
                songaudio=True,
                format_id=format_id,
                title=title,
            )

        except Exception as e:

            return await mystic.edit_text(_["song_9"].format(e))

        med = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=x["uploader"],
        )

        await mystic.edit_text(_["song_11"])

        await app.send_chat_action(
            chat_id=CallbackQuery.message.chat.id,
            action=enums.ChatAction.UPLOAD_AUDIO,
        )

        try:

            await CallbackQuery.edit_message_media(media=med)

        except Exception as e:

            print(e)

            return await mystic.edit_text(_["song_10"])

        os.remove(filename)
"""
