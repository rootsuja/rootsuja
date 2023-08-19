# @Rizzvbss | @Kenapanan | @SharingUserbot | Zaid-Userbot
# © @KynanSupport


import asyncio
import os
from io import BytesIO

from pyrogram import filters
from pyrogram.enums import MessageMediaType, MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import InputMediaPhoto

from . import *

__MODULE__ = "convert"
__HELP__ = f"""
✘ Bantuan Untuk Convert

๏ Perintah: <code>{cmd}toaudio</code> [reply to video]
◉ Penjelasan: Untuk merubah video menjadi audio mp3.
           
๏ Perintah: <code>{cmd}toanime</code> [reply to photo]
◉ Penjelasan: Untuk merubah foto menjadi anime.

๏ Perintah: <code>{cmd}toimg</code> [balas stikers]
◉ Penjelasan: Untuk membuat nya menjadi foto.
"""


@bots.on_message(filters.me & filters.command("toanime", cmd))
async def _(client, message):
    Tm = await eor(message, "<b>Tunggu sebentar...</b>")
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                get_photo = message.reply_to_message.photo.file_id
            if message.reply_to_message.sticker:
                pass
            if message.reply_to_message.animation:
                pass
            path = await client.download_media(message.reply_to_message)
            with open(path, "rb") as f:
                content = f.read()
            os.remove(path)
            get_photo = BytesIO(content)
        elif message.command[1] in ["foto", "profil", "photo"]:
            chat = (
                message.reply_to_message.from_user
                or message.reply_to_message.sender_chat
            )
            get = await client.get_chat(chat.id)
            photo = get.photo.big_file_id
            get_photo = await client.download_media(photo)
    else:
        if len(message.command) < 2:
            return await Tm.edit(
                "Balas ke foto dan saya akan merubah foto anda menjadi anime"
            )
        get = await client.get_chat(message.command[1])
        photo = get.photo.big_file_id
        get_photo = await client.download_media(photo)
    await client.unblock_user("@qq_neural_anime_bot")
    Tm_S = await client.send_photo("@qq_neural_anime_bot", get_photo)
    await Tm.edit("<b>Sedang diproses...</b>")
    await Tm_S.delete()
    await asyncio.sleep(30)
    info = await client.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in client.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(InputMediaPhoto(anime.photo.file_id))
    if anime_photo:
        await client.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

    else:
        await client.send_message(
            message.chat.id,
            f"<b>gagal merubah {file} menjadi gambar anime</b>",
            reply_to_message_id=message.id,
        )
        return await client.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@bots.on_message(filters.me & filters.command("toaudio", cmd))
async def _(client, message):
    replied = message.reply_to_message
    Tm = await eor(message, "<code>Processing...</code>")
    if not replied:
        await Tm.edit("<code>Mohon Balas Ke Video</code>")
        return
    if replied.media == MessageMediaType.VIDEO:
        await Tm.edit("<code>Converting . . .</code>")
        file = await client.download_media(
            message=replied,
            file_name="naya/resources/",
        )
        out_file = f"{file}.mp3"
        try:
            await Tm.edit("<code>Processing. . .</code>")
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await run_cmd(cmd)
            await Tm.edit("<code>Uploading . . .</code>")
            await client.send_audio(
                message.chat.id,
                audio=out_file,
                reply_to_message_id=message.id,
            )
            await Tm.delete()
        except BaseException as e:
            await Tm.edit(f"<code>INFO:</code> {e}")
    else:
        await Tm.edit("<code>Mohon Balas Ke Video</code>")
        return
