# @Rizzvbss | @Kenapanan | @SharingUserbot | Zaid-Userbot
# @KynanSupport

import random
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatType

from . import *


# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    return dt_string.split(" ")


def dt_tom():
    return (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )


today = str(dt()[0])
tomorrow = str(dt_tom())


@bots.on_message(filters.me & filters.command(["couple"], cmd))
async def couple(client, message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text(
            "Perintah ini hanya dapat digunakan dalam grup."
        )
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            async for i in client.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                return await message.reply_text("Tidak cukup pengguna")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await client.get_users(c1_id)).mention
            c2_mention = (await client.get_users(c2_id)).mention

            couple_selection_message = f"""**Pasangan :**

{c1_mention} + {c2_mention} = 😘
__Pasangan baru dipilih {tomorrow}__"""
            await client.send_message(message.chat.id, text=couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        else:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await client.get_users(c1_id)).first_name
            c2_name = (await client.get_users(c2_id)).first_name
            couple_selection_message = f"""Pasangan :**

[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = 😘
__Pasangan baru dipilih {tomorrow}__"""
            await client.send_message(message.chat.id, text=couple_selection_message)
    except Exception as e:
        print(e)
        await message.reply_text(e)


__MODULE__ = "couple"
__HELP__ = f"""
✘ Bantuan Untuk Couple

๏ Perintah: <code>{cmd}couple</code>
◉ Penjelasan: Melihat pasangan dalam grup.
"""
