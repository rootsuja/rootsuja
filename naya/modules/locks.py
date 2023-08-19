# @Rizzvbss | @Kenapanan | @SharingUserbot | Zaid-Userbot
# © @KynanSupport


from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import (ChatAdminRequired,
                                                        ChatNotModified)
from pyrogram.types import ChatPermissions, Message

from . import *

incorrect_parameters = (
    f"Parameter salah, gunakan `help locks` untuk melihat contoh penggunaan"
)
data = {
    "msg": "can_send_messages",
    "stickers": "can_send_other_messages",
    "gifs": "can_send_other_messages",
    "media": "can_send_media_messages",
    "games": "can_send_other_messages",
    "inline": "can_send_other_messages",
    "urls": "can_add_web_page_previews",
    "polls": "can_send_polls",
    "info": "can_change_info",
    "invite": "can_invite_users",
    "pin": "can_pin_messages",
}


async def current_chat_permissions(client: Client, chat_id):
    perms = []
    perm = (await client.get_chat(chat_id)).permissions
    if perm.can_send_messages:
        perms.append("can_send_messages")
    if perm.can_send_media_messages:
        perms.append("can_send_media_messages")
    if perm.can_send_other_messages:
        perms.append("can_send_other_messages")
    if perm.can_add_web_page_previews:
        perms.append("can_add_web_page_previews")
    if perm.can_send_polls:
        perms.append("can_send_polls")
    if perm.can_change_info:
        perms.append("can_change_info")
    if perm.can_invite_users:
        perms.append("can_invite_users")
    if perm.can_pin_messages:
        perms.append("can_pin_messages")
    return perms


async def tg_lock(
    client: Client,
    message: Message,
    parameter,
    permissions: list,
    perm: str,
    lock: bool,
):
    if lock:
        if perm not in permissions:
            return await message.edit_text(f"🔒 `{parameter}` **Sudah di-lock!**")
        permissions.remove(perm)
    else:
        if perm in permissions:
            return await message.edit_text(f"🔓 `{parameter}` **Sudah di-unlock!**")
        permissions.append(perm)
    permissions = {perm: True for perm in list(set(permissions))}
    try:
        await client.set_chat_permissions(
            message.chat.id, ChatPermissions(**permissions)
        )
    except ChatNotModified:
        return await message.edit_text(f"Gunakan lock, terlebih dahulu.")
    except ChatAdminRequired:
        return await message.edit_text("`Anda harus menjadi admin disini.`")
    await message.edit_text(
        (
            f"🔒 **Locked untuk non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            if lock
            else f"🔒 **Unlocked untuk non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )
    )


@bots.on_message(filters.command(["lock", "unlock"], cmd) & filters.me)
async def locks_func(client: Client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(incorrect_parameters)
    chat_id = message.chat.id
    parameter = message.text.strip().split(None, 1)[1].lower()
    state = message.command[0].lower()
    if parameter not in data and parameter != "all":
        return await message.edit_text(incorrect_parameters)
    permissions = await current_chat_permissions(client, chat_id)
    if parameter in data:
        await tg_lock(
            client,
            message,
            parameter,
            permissions,
            data[parameter],
            bool(state == "lock"),
        )
    elif parameter == "all" and state == "lock":
        try:
            await client.set_chat_permissions(chat_id, ChatPermissions())
            await message.edit_text(
                f"🔒 **Locked untuk non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
        except ChatAdminRequired:
            return await message.edit_text("`anda harus menjadi admin disini.`")
        except ChatNotModified:
            return await message.edit_text(
                f"🔒 **Berhasil di-Lock!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
            )
    elif parameter == "all" and state == "unlock":
        try:
            await client.set_chat_permissions(
                chat_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_send_polls=True,
                    can_change_info=False,
                    can_invite_users=True,
                    can_pin_messages=False,
                ),
            )
        except ChatAdminRequired:
            return await message.edit_text("`Anda harus menjadi admin disini`")
        await message.edit(
            f"🔒 **Unlocked untuk non-admin!**\n  **Type:** `{parameter}`\n  **Chat:** {message.chat.title}"
        )

    elif parameter == "all" and state == "unlock":
        await client.set_chat_permissions(
            chat_id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False,
            ),
        )
        await eor(
            message, f"🔓 <b>Unlock untuk semua</b> <code>{message.chat.title}</code>"
        )


@bots.on_message(filters.command("locks", cmd) & filters.me)
async def locktypes(client, message):
    permissions = await current_chat_permissions(client, message.chat.id)

    if not permissions:
        return await eor(message, "<code>Anda bukan Admin.</code>.")

    perms = "".join(f"__<b>{i}</b>__\n" for i in permissions)
    await eor(message, perms)


__MODULE__ = "locks"
__HELP__ = f"""
✘ Bantuan Untuk Locks

๏ Perintah: <code>{cmd}lock or unlock</code> [query]
◉ Penjelasan: Untuk mengunci atau membuka izin grup.

๏ Perintah: <code>{cmd}locks</code>
◉ Penjelasan: Untuk izin grup.

Spesifikasi Kunci : Locks / Unlocks: <code>msg</code> | <code>media</code> | <code>stickers</code> | <code>polls</code> | <code>info</code>  | <code>invite</code> | <code>url</code> |<code>pin</code> | <code>all</code>.
"""
