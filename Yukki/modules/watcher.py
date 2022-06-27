import re
import time

from pyrogram import filters
from pyrogram.types import Message

from Yukki import app, botid, botname, botusername
from Yukki.database import add_served_chat, is_afk, remove_afk
from Yukki.helpers import get_readable_time, put_cleanmode

chat_watcher_group = 1

@app.on_message(
    ~filters.edited & ~filters.me & ~filters.bot & ~filters.via_bot,
    group=chat_watcher_group,
)
async def chat_watcher_func(_, message):
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.first_name
    if message.entities:
        possible = ["/afk", f"/afk@{botusername}"]
        message_text = message.text or message.caption
        for entity in message.entities:
            if entity.type == "bot_command":
                if (message_text[0 : 0 + entity.length]) in possible:
                    return

    msg = ""
    replied_user_id = 0

    # Self AFK
    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                msg += f"**{user_name[:25]}** is back online and was away for {seenago}\n\n"
            if afktype == "text_reason":
                msg += f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n"
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\n",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\n",
                    )
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]}** is back online and was away for {seenago}\n\nReason: `{reasonafk}`\n\n",
                    )
        except:
            msg += f"**{user_name[:25]}** is back online\n\n"
        
    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = (
                message.reply_to_message.from_user.first_name
            )
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time(
                        (int(time.time() - timeafk))
                    )
                    if afktype == "text":
                        msg += f"**{replied_first_name[:25]}** is AFK since {seenago}\n\n"
                    if afktype == "text_reason":
                        msg += f"**{replied_first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\n",
                            )
                        else:
                            send = await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\n",
                            )
                        else:
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                            )
                except Exception as e:
                    msg += f"**{replied_first_name}** is AFK\n\n"
        except:
            pass

    # If username or mentioned user is AFK
    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == "mention":
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{user.first_name[:25]}** is AFK since {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**{user.first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                    except:
                        msg += (
                            f"**{user.first_name[:25]}** is AFK\n\n"
                        )
            elif (entity[j].type) == "text_mention":
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{first_name[:25]}** is AFK since {seenago}\n\n"
                        if afktype == "text_reason":
                            msg += f"**{first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\n",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]}** is AFK since {seenago}\n\nReason: `{reasonafk}`\n\n",
                                )
                    except:
                        msg += f"**{first_name[:25]}** is AFK\n\n"
            j += 1
    if msg != "":
        try:
            send =  await message.reply_text(
                msg, disable_web_page_preview=True
            )
        except:
            return
    try:
        await put_cleanmode(message.chat.id, send.message_id)
    except:
        return


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == botid:
                send =  await message.reply_text(
                    f"Thanks for having me in {message.chat.title}\n\n{botname} is alive."
                )
                await put_cleanmode(message.chat.id, send.message_id)
        except:
            return


@app.on_message(filters.command(["repo"])& filters.private)
async def run(client, message):
    await message.reply_text(f"Look at sky \n Sky is Blue 💙")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0AFiqLFq96XquupWkC3Wjww8cIo8HwACRAIAAtSXSEXU4M20BCBnFCQE")
    await message.reply_text(f"Now look at you \n There's No One Ugly as You 😝")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0FZiqLivDE15hr0iUXXB3uLKkm4iGQACvQIAAm9fSEXTjPhY1VGe5SQE")
    await message.reply_text(f"I Really Think You should be in the Zoo 😂")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0FliqLkzC0-vr0HKeCxg-QfbH8IW0gACbgIAAgnDSEVqYh91csOLqyQE")
    await message.reply_text(f"Don't worry I'll be there too 🥺")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0F9iqLoP10v9cGFlNDYlvMkf5EJcHgACDgIAApwgSUXoPrEi4_q4tyQE")
    await message.reply_text(f"But Laughing at you!!! ")
    await app.send_sticker(message.chat.id,"CAACAgUAAxkBAAFC0GJiqLqM2c0OK0MM45QaNtMwYlpU9AACuwUAAg2iqVdfW2GdjZSKYSQE")
    await message.reply_text(f"Ask for repo again And \n I will hit you with a shoe 🌝")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0GZiqLubtDfUiSZOCibf8BS7LzsnuwACSgMAAlopSEUBme_jF0ul2yQE")
    await message.reply_text(f"If i do... \n Please You don't Cry ")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0GxiqLzmpch1zZbA87pClhIrqg1jGgACxwMAAs72QEUySsl-a4Af0CQE")
    await message.reply_text(f"And GOOD BYE ! 🎋💕")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0G9iqL0J8n28bWQS4_U3ziLujmHOoAACXgIAAm53SEW3PHkJlNtQ9iQE")

@app.on_message(filters.command(["ping"]))
async def on_start(_, message: Message):
    bot_uptime = int(time.time() - boot)
    Uptime = get_readable_time(bot_uptime)
    await message.reply_photo(photo="RANDOM", caption=
        f"{botname} is alive and working good.\n\nUptime : {Uptime}"
    )
