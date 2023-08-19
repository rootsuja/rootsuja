# @Rizzvbss | @Kenapanan | @SharingUserbot | Zaid-Userbot
# @KynanSupport

import asyncio
from io import BytesIO

from pyrogram import filters

from . import *


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@bots.on_message(filters.me & filters.command(["carbon"], cmd))
async def carbon_func(client, message):
    text = (
        message.text.split(None, 1)[1]
        if len(
            message.command,
        )
        != 1
        else None
    )
    if message.reply_to_message:
        text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return await eor(message, "`Berikan saya teks...`")
    ex = await eor(message, "`Processing . . .`")
    carbon = await make_carbon(text)
    await ex.edit("`Uploading . . .`")
    await asyncio.gather(
        ex.delete(),
        client.send_photo(
            message.chat.id,
            carbon,
            caption=f"**Carbonised by** {client.me.mention}",
            reply_to_message_id=ReplyCheck(message),
        ),
    )
    carbon.close()


__MODULE__ = "carbon"
__HELP__ = f"""
✘ Bantuan Untuk Carbon

๏ Perintah: <code>{cmd}carbon</code> [balas pesan]
◉ Penjelasan: Untuk membuat teks menjadi carbonara.
"""
