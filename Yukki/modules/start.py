import time
import random
import asyncio

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import MessageNotModified

from Yukki import app, boot, botname, botusername
from Yukki.database.cleanmode import cleanmode_off, cleanmode_on, is_cleanmode_on
from Yukki.helpers import get_readable_time, put_cleanmode, settings_markup, RANDOM, HELP_TEXT


@app.on_message(filters.command(["start", "settings"]) & filters.group & ~filters.edited)
async def on_start(_, message: Message):
    bot_uptime = int(time.time() - boot)
    Uptime = get_readable_time(bot_uptime)
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Help ❔",
                    url=f"https://t.me/{botusername}?start=help",
                ),
                InlineKeyboardButton(
                    text="Settings❓",
                    callback_data="settings_callback",
                ),
            ]
        ]
    )
    image = random.choice(RANDOM)
    send = await message.reply_photo(image, caption=f"Version⌱ P.C3\n\nUptime⌱ {Uptime}", reply_markup=upl)
    await put_cleanmode(message.chat.id, send.message_id)
    

@app.on_message(filters.command(["help"]) & filters.group & ~filters.edited)
async def on_help(_, message: Message):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="⛑️Help Section⛑️",
                    url=f"https://t.me/{botusername}?start=help",
                ),
            ]
        ]
    )
    send = await message.reply_text("Contact me in PM for help.", reply_markup=upl)
    await put_cleanmode(message.chat.id, send.message_id)

@app.on_message(filters.command(["start"]) & filters.private & ~filters.edited)
async def on_private_start(_, message: Message):
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            return await message.reply_text(HELP_TEXT)
    else:
        bot_uptime = int(time.time() - boot)
        Uptime = get_readable_time(bot_uptime)
        upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Add ❔",
                    url=f"https://t.me/C2_Probot?startgroup=true",
                ),
                InlineKeyboardButton(
                    text="Chat ❓",
                    url=f"https://t.me/+LuNfF7pzIggyNWE1",
                ),
            ]
        ]
    )
        image = random.choice(RANDOM)
        await message.reply_photo(image, caption=f"Just a Advanced AFK Bot \n\nActive since: {Uptime}", reply_markup=upl)

@app.on_message(filters.command(["help"]) & filters.private & ~filters.edited)
async def on_private_help(_, message: Message):
    return await message.reply_text(HELP_TEXT)
        
@app.on_callback_query(filters.regex("close"))
async def on_close_button(client, CallbackQuery):
    await CallbackQuery.answer()
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex("cleanmode_answer"))
async def on_cleanmode_button(client, CallbackQuery):
    await CallbackQuery.answer("What's CleanMode ⁉️\n\nWhen activated, Bot will delete its message after 1 Mins to make your chat clean and clear.", show_alert=True)

@app.on_callback_query(filters.regex("settings_callback"))
async def on_settings_button(client, CallbackQuery):
    await CallbackQuery.answer()
    status = await is_cleanmode_on(CallbackQuery.message.chat.id)
    buttons = settings_markup(status)
    return await CallbackQuery.edit_message_text(f"⚙️ C.C. CleanMode settings:\n\n🎗️ Tap on Buttons below to turn CleanMode ON or OFF", reply_markup=InlineKeyboardMarkup(buttons),)

@app.on_callback_query(filters.regex("CLEANMODE"))
async def on_cleanmode_change(client, CallbackQuery):
    admin = await app.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    if admin.status in ["creator", "administrator"]:
        pass
    else:
        return await CallbackQuery.answer("Only Admins can perform this action.", show_alert=True)
    await CallbackQuery.answer()
    status = None
    if await is_cleanmode_on(CallbackQuery.message.chat.id):
        await cleanmode_off(CallbackQuery.message.chat.id)
    else:
        await cleanmode_on(CallbackQuery.message.chat.id)
        status = True
    buttons = settings_markup(status)
    try:
        return await CallbackQuery.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
    except MessageNotModified:
        return


@app.on_message(filters.command(["repo"])& filters.private)
async def run(client, message):
    await message.reply_text(f"Look at sky \n Sky is Blue 💙")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0AFiqLFq96XquupWkC3Wjww8cIo8HwACRAIAAtSXSEXU4M20BCBnFCQE")
    await asyncio.sleep(3)
    await message.reply_text(f"Now look at you \n There's No One Ugly as You 😝")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0FZiqLivDE15hr0iUXXB3uLKkm4iGQACvQIAAm9fSEXTjPhY1VGe5SQE")
    await asyncio.sleep(3)
    await message.reply_text(f"I Really Think You should be in the Zoo 😂")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0FliqLkzC0-vr0HKeCxg-QfbH8IW0gACbgIAAgnDSEVqYh91csOLqyQE")
    await asyncio.sleep(3)
    await message.reply_text(f"Don't worry I'll be there too 🥺")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0F9iqLoP10v9cGFlNDYlvMkf5EJcHgACDgIAApwgSUXoPrEi4_q4tyQE")
    await asyncio.sleep(3)
    await message.reply_text(f"But Laughing at you!!! ")
    await app.send_sticker(message.chat.id,"CAACAgUAAxkBAAFC0GJiqLqM2c0OK0MM45QaNtMwYlpU9AACuwUAAg2iqVdfW2GdjZSKYSQE")
    await asyncio.sleep(3)
    await message.reply_text(f"Ask for repo again And \n I will hit you with a shoe 🌝")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0GZiqLubtDfUiSZOCibf8BS7LzsnuwACSgMAAlopSEUBme_jF0ul2yQE")
    await asyncio.sleep(3)
    await message.reply_text(f"If i do... \n Please You don't Cry ")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0GxiqLzmpch1zZbA87pClhIrqg1jGgACxwMAAs72QEUySsl-a4Af0CQE")
    await asyncio.sleep(3)
    await message.reply_text(f"And GOOD BYE !🎋💕")
    await app.send_sticker(message.chat.id,"CAACAgEAAxkBAAFC0G9iqL0J8n28bWQS4_U3ziLujmHOoAACXgIAAm53SEW3PHkJlNtQ9iQE")
    await message.reply_text(f"THE \n       END")


@app.on_message(filters.command(["ping"]))
async def on_start(_, message: Message):
    bot_uptime = int(time.time() - boot)
    Uptime = get_readable_time(bot_uptime)
    image = random.choice(RANDOM)
    await message.reply_photo(image, caption=
        f"{botname} is alive and working good.\nPing : 89.345ms\nUptime : {Uptime}"
    )
@app.on_message(filters.command(["dsp"]))
async def on_private_help(_, message: Message):
    return await message.reply_text(f"✅ ALIVE.)
