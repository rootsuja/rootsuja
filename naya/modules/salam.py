# @Rizzvbss | @Kenapanan | @SharingUserbot | Zaid-Userbot
# @KynanSupport


import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from . import *


@bots.on_message(filters.command("p", cmd) & filters.me)
async def salamone(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Assalamualaikum...",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@bots.on_message(filters.command("pe", cmd) & filters.me)
async def salamdua(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Assalamualaikum Warahmatullahi Wabarakatuh",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@bots.on_message(filters.command("l", cmd) & filters.me)
async def jwbsalam(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Wa'alaikumsalam...",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@bots.on_message(filters.command("wl", cmd) & filters.me)
async def jwbsalamlngkp(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Wa'alaikumsalam Warahmatullahi Wabarakatuh",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@bots.on_message(filters.command("as", cmd) & filters.me)
async def salamarab(client: Client, message: Message):
    xx = await edit_or_reply(message, "Salam Dulu Gua..")
    await asyncio.sleep(2)
    await xx.edit("السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ")


__MODULE__ = "salam"
__HELP__ = f"""
✘ Bantuan Untuk Salam 🌞

➜ Perintah: <code>{{cmd}}p</code>
    Penjelasan: Coba sendiri.

➜ Perintah: <code>{{cmd}}pe</code>
    Penjelasan: Coba sendiri.

➜ Perintah: <code>{{cmd}}l</code>
    Penjelasan: Coba sendiri.

➜ Perintah: <code>{{cmd}}wl</code>
    Penjelasan: Coba sendiri.

➜ Perintah: <code>{{cmd}}as</code>
    Penjelasan: Coba sendiri.
"""
