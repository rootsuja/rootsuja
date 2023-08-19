# @Rizzvbss | @Kenapanan | @SharingUserbot | Zaid-Userbot
# @KynanSupport


import asyncio
import datetime
import re
import sys
from datetime import datetime
from os import environ, execle

import dotenv
import heroku3
import urllib3

HAPP = None
import urllib3
from pyrogram.raw.functions import Ping
from pyrogram.types import *

from naya.config import *

from . import *
from .ping import START_TIME, _human_time_duration
from .system import anu_heroku

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

photo = "naya/resources/logo.jpg"


@bots.on_message(filters.command(["help", "alive"], cmd) & filters.me)
async def _(client, message):
    if message.command[0] == "alive":
        text = f"user_alive_command {message.id} {message.from_user.id}"
    if message.command[0] == "help":
        text = "user_help_command"
    try:
        x = await client.get_inline_bot_results(app.me.username, text)
        for m in x.results:
            await message.reply_inline_bot_result(x.query_id, m.id)
    except Exception as error:
        await message.reply(error)


@app.on_inline_query(filters.regex("^user_alive_command"))
async def _(client, inline_query):
    inline_query.query.split()
    expired = "__none__"
    status1 = "premium"
    expired = "__none__"
    for bot in botlist:
        users = 0
        group = 0
        async for dialog in bot.get_dialogs():
            if dialog.chat.type == enums.ChatType.PRIVATE:
                users += 1
            elif dialog.chat.type in (
                enums.ChatType.GROUP,
                enums.ChatType.SUPERGROUP,
            ):
                group += 1
        if bot.me.id in DEVS:
            status = "founder"
        elif bot.me.id == OWNER:
            status = "owner"
        else:
            status = "admin"
        start = datetime.now()
        await bot.invoke(Ping(ping_id=0))
        ping = (datetime.now() - start).microseconds / 1000
        uptime_sec = (datetime.utcnow() - START_TIME).total_seconds()
        uptime = await _human_time_duration(int(uptime_sec))
        msg = f"""
<b>Naya-Pyro</b>
     <b>status:</b> <code>{status1}[{status}]</code>
          <b>dc_id:</b> <code>{bot.me.dc_id}
          <b>ping_dc:</b> <code>{ping} ms</code>
          <b>peer_users:</b> <code>{users} users</code>
          <b>peer_group:</b> <code>{group} group</code>
          <b>uptime:</b> <code>{uptime}</code>
          <b>expired:</b> <code>{expired}</code>
"""
        await client.answer_inline_query(
            inline_query.id,
            cache_time=300,
            results=[
                InlineQueryResultArticle(
                    title="💬",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="Close", callback_data="alv_cls"
                                ),
                                InlineKeyboardButton(
                                    text="Support",
                                    url="https://t.me/kynansupport",
                                ),
                            ]
                        ]
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            ],
        )


@app.on_inline_query(filters.regex("^user_help_command"))
async def _(client, inline_query):
    msg = f"<b>❏ Menu Bantuan\n├ Modules: {len(CMD_HELP)}\n╰ Perintah: <code>{cmd}</code></b>"
    await client.answer_inline_query(
        inline_query.id,
        cache_time=300,
        results=[
            (
                InlineQueryResultArticle(
                    title="Help Menu!",
                    reply_markup=InlineKeyboardMarkup(
                        paginate_modules(0, CMD_HELP, "help")
                    ),
                    input_message_content=InputTextMessageContent(msg),
                )
            )
        ],
    )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def _(client, callback_query):
    mod_match = re.match(r"help_module\((.+?)\)", callback_query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", callback_query.data)
    next_match = re.match(r"help_next\((.+?)\)", callback_query.data)
    back_match = re.match(r"help_back", callback_query.data)
    if mod_match:
        module = mod_match[1].replace(" ", "_")
        text = f"<b>{CMD_HELP[module].__HELP__}</b>\n"
        button = [[InlineKeyboardButton("Kembali", callback_data="help_back")]]
        await callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
    prev_text = f"<b>❏ Menu Bantuan\n├ Modules: {len(CMD_HELP)}\n╰ Perintah: <code>{cmd}</code></b>"
    if prev_match:
        curr_page = int(prev_match[1])
        await callback_query.edit_message_text(
            text=prev_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, CMD_HELP, "help")
            ),
            disable_web_page_preview=True,
        )
    next_text = f"<b>❏ Menu Bantuan\n├ Modules: {len(CMD_HELP)}\n╰ Perintah: <code>{cmd}</code></b>"
    if next_match:
        next_page = int(next_match[1])
        await callback_query.edit_message_text(
            text=next_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, CMD_HELP, "help")
            ),
            disable_web_page_preview=True,
        )
    back_text = f"<b>❏ Menu Bantuan\n├ Modules: {len(CMD_HELP)}\n╰ Perintah: <code>{cmd}</code></b>"
    if back_match:
        await callback_query.edit_message_text(
            text=back_text,
            reply_markup=InlineKeyboardMarkup(paginate_modules(0, CMD_HELP, "help")),
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["user"]) & filters.private)
async def usereee(_, message):
    user_id = message.from_user.id
    if user_id not in (OWNER, DEVS):
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya OWNER yang bisa menggunakan perintah ini"
        )
    count = 0
    user = ""
    for X in botlist:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
 ╰ ID: <code>{X.me.id}</code>
"""
        except BaseException:
            pass
    if len(str(user)) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")


@app.on_callback_query(filters.regex("^alv_cls"))
async def _(cln, cq):
    cq.data.split()
    unPacked = unpackInlineMessage(cq.inline_message_id)
    for bot in botlist:
        if cq.from_user.id == int(bot.me.id):
            await bot.delete_messages(
                unPacked.chat_id, [int(bot.me.id), unPacked.message_id]
            )


@app.on_callback_query(filters.regex("cl_ad"))
async def _(_, query: CallbackQuery):
    await query.message.delete()


@app.on_callback_query(filters.regex("multi"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        "<b>Disini kamu bisa menambahkan, menghapus serta melihat variabel dan value, seperti OPENAI_API, SESSION2-SESSION10.</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(text="Hapus Variabel", callback_data="hapus"),
                ],
                [
                    InlineKeyboardButton(text="Cek Variabel", callback_data="get"),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="setong"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("pm"))
async def _(_, query: CallbackQuery):
    await query.message.delete()
    await query.message.reply_photo(
        photo=photo,
        caption="<b> ☺️ Fitur ini akan hadir dalam beberapa pekan\n\nTunggu update nya di @KynanSupport.</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Kembali", callback_data="setong"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("log"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        log = await app.ask(
            user_id,
            "<b>Silakan masukkan botlog grup id anda.\nContoh : -100XXXXXX\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, log.text):
        return

    botlog = log.text
    await set_botlog(user_id, botlog)
    buttons = [
        [
            InlineKeyboardButton(text="Kembali", callback_data="multi"),
            InlineKeyboardButton("Tutup", callback_data="cl_ad"),
        ],
    ]
    await app.send_message(
        user_id,
        f"**Berhasil mengatur botlog grup anda menjadi `{botlog}`.**",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("inpo"))
async def _(_, query):
    await query.message.delete()
    await query.message.reply_photo(
        photo=photo,
        caption="<b> ☺️ Halo mek saya adalah Naya-Pyro Premium\nLu minat punya repo kek gini ? Dateng ae mek ke @KynanSupport.</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Support", url="https://t.me/kynansupport")],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("setong"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        f"""
    <b> ☺️Halo aku adalah <a href=tg://openmessage?user_id={query.message.from_user.id}>{query.message.from_user.first_name} {query.message.from_user.last_name or ''}</a> asisten mu yang siap membantu kamu ! \n Apa yang kamu butuhkan ?.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Multi Client", callback_data="multi"),
                    InlineKeyboardButton(text="Restart", callback_data="retor"),
                ],
                [
                    InlineKeyboardButton(text="Logger", callback_data="log"),
                    InlineKeyboardButton(text="PM Permit", callback_data="pm"),
                ],
                [
                    InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                ],
            ]
        ),
    )


@app.on_callback_query(filters.regex("restart"))
async def _(_, query: CallbackQuery):
    try:
        await query.edit_message_text("<b>Processing...</b>")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await asyncio.sleep(2)
    await query.edit_message_text(f"✅ <b>{app.me.mention} Berhasil Di Restart.</b>")
    args = [sys.executable, "-m", "naya"]
    execle(sys.executable, *args, environ)


@app.on_callback_query(filters.regex("retor"))
async def _(_, query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton(text="✅ Restart", callback_data="restart"),
            InlineKeyboardButton("❌ Tidak", callback_data="cl_ad"),
        ],
    ]
    await query.edit_message_text(
        "<b>Apakah kamu yakin ingin Melakukan Restart ?</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_message(filters.command(["start"]))
async def _(_, message):
    user_id = message.from_user.id
    _ubot = [bot.me.id for bot in botlist]
    if user_id not in _ubot and user_id not in DEVS:
        return await message.reply_photo(
            photo=photo,
            caption=f"""
<b>👋 Halo Jeng <a href=tg://openmessage?user_id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a> !
💭 Apa ada yang bisa gue banting ?
💡 Gua Milik Owner Dibawah Ni.</b>
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="👮‍♂ Owner", user_id=OWNER),
                        InlineKeyboardButton(text="Info", callback_data="inpo"),
                    ],
                    [InlineKeyboardButton("Tutup", callback_data="cl_ad")],
                ]
            ),
        )
    else:
        await message.reply_photo(
            photo=photo,
            caption=f"""
<b>👋 Halo <a href=tg://openmessage?user_id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a> !
💭 Apa ada yang bisa saya bantu ?
💡 Silakan pilih tombol dibawah untuk kamu perlukan.
</b>""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Pengaturan", callback_data="setong"),
                    ],
                    [InlineKeyboardButton("Tutup", callback_data="cl_ad")],
                ]
            ),
        )


@app.on_message(filters.command(["getotp", "getnum"]) & filters.private)
async def _(_, message):
    user_id = message.from_user.id
    if len(message.command) < 2:
        return await app.send_message(
            message.chat.id,
            f"<code>{message.text} user_id userbot yang aktif</code>",
            reply_to_message_id=message.id,
        )
    elif user_id not in (OWNER, DEVS):
        return await message.reply(
            "❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya OWNER yang bisa menggunakan perintah ini"
        )
    try:
        for X in botlist:
            if int(message.command[1]) == X.me.id:
                if message.command[0] == "getotp":
                    async for otp in X.search_messages(777000, limit=1):
                        if otp.text:
                            return await app.send_message(
                                message.chat.id,
                                otp.text,
                                reply_to_message_id=message.id,
                            )
                        else:
                            return await app.send_message(
                                message.chat.id,
                                "<code>Kode Otp Tidak Di Temukan</code>",
                                reply_to_message_id=message.id,
                            )
                elif message.command[0] == "getnum":
                    return await app.send_message(
                        message.chat.id,
                        X.me.phone_number,
                        reply_to_message_id=message.id,
                    )
    except Exception as error:
        return await app.send_message(
            message.chat.id, error, reply_to_message_id=message.id
        )


@app.on_callback_query(filters.regex("sesi"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        var = await app.ask(
            user_id,
            "<b>Silakan masukkan variabel.\nContoh : SESSION2\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, var.text):
        return

    variable = var.text

    try:
        val = await app.ask(
            user_id,
            "<b>Silakan masukkan value.\nContoh : 02ODJDOEMXNXXXXX\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, val.text):
        return

    value = val.text
    if "HEROKU_APP_NAME" in os.environ and "HEROKU_API_KEY" in os.environ:
        api_key = os.environ["HEROKU_API_KEY"]
        app_name = os.environ["HEROKU_APP_NAME"]
        heroku = heroku3.from_key(api_key)
        hero = heroku.apps()[app_name]
        config_vars = hero.config()
        config_vars[variable] = value
        buttons = [
            [
                InlineKeyboardButton(text="Kembali", callback_data="multi"),
                InlineKeyboardButton("Tutup", callback_data="cl_ad"),
            ],
        ]
        await app.send_message(
            user_id,
            f"**Berhasil mengatur variable `{variable}` dengan value `{value}`\n\nJangan lupa untuk melakukan restart setelah menambah variabel baru.**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        # herotod.update_config(config_vars)
    else:
        path = ".env"
        with open(path, "a") as file:
            file.write(f"\n{variable}={value}")
        if dotenv.get_key(path, variable):
            buttons = [
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            await app.send_message(
                user_id,
                f"**Berhasil mengatur variable `{variable}` dengan value `{value}`\n\nJangan lupa untuk melakukan restart setelah menambah variabel baru.**",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


async def batal(query, text):
    if text.startswith("/cancel"):
        user_id = query.from_user.id
        await app.send_message(user_id, "<b>Dibatalkan !</b>")
        return True
    return False


@app.on_callback_query(filters.regex("hapus"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        ver = await app.ask(
            user_id,
            "<b>Silakan masukkan variabel.\nContoh : SESSION2\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, ver.text):
        return

    pariabel = ver.text
    if "HEROKU_APP_NAME" in os.environ and "HEROKU_API_KEY" in os.environ:
        api_key = os.environ["HEROKU_API_KEY"]
        app_name = os.environ["HEROKU_APP_NAME"]
        heroku = heroku3.from_key(api_key)
        hero = heroku.apps()[app_name]
        config_vars = hero.config()
        del config_vars[pariabel]
        buttons = [
            [
                InlineKeyboardButton(text="Kembali", callback_data="multi"),
                InlineKeyboardButton("Tutup", callback_data="cl_ad"),
            ],
        ]
        await app.send_message(
            user_id,
            f"**Berhasil menghapus variable `{pariabel}`\n\nJangan lupa untuk melakukan restart setelah menghapus variabel.**",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        path = ".env"
        dotenv.unset_key(path, pariabel)

        if dotenv.get_key(path, pariabel) is None:
            buttons = [
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            await app.send_message(
                user_id,
                f"**Berhasil menghapus variable `{pariabel}`\n\nJangan lupa untuk melakukan restart setelah menghapus variabel.**",
                reply_markup=InlineKeyboardMarkup(buttons),
            )


@app.on_callback_query(filters.regex("get"))
async def _(_, query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    try:
        get = await app.ask(
            user_id,
            "<b>Silakan masukkan variabel.\nContoh : SESSION2\n\nKetik /cancel untuk membatalkan proses.</b>",
            timeout=120,
        )
    except asyncio.TimeoutError:
        return await app.send_message(user_id, "Waktu Telah Habis")

    if await batal(query, get.text):
        return

    variable = get.text
    if anu_heroku():
        if variable in os.environ:
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            return await app.send_message(
                user_id,
                f"<b>{variable}:</b> <code>{os.environ[variable]}</code>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            return await app.send_message(
                user_id,
                f"<b>Tidak ada <code>{variable}</code> ditemukan.</b>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
    else:
        path = ".env"
        if output := dotenv.get_key(path, variable):
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            await app.send_message(
                user_id,
                f"<b>{variable}:</b> <code>{os.environ[variable]}</code>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            buttons = [
                [
                    InlineKeyboardButton(text="Tambah Variabel", callback_data="sesi"),
                    InlineKeyboardButton(
                        text="Hapus Variabel", callback_data="remsesi"
                    ),
                ],
                [
                    InlineKeyboardButton(text="Kembali", callback_data="multi"),
                    InlineKeyboardButton("Tutup", callback_data="cl_ad"),
                ],
            ]
            return await app.send_message(
                user_id,
                f"<b>Tidak ada <code>{variable}</code> ditemukan.</b>",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
