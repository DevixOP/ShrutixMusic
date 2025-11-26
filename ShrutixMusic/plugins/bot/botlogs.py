# copyright ©️ by Akash Dakshwanshi 

import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import LOGGER_ID
from ShrutixMusic import nand
from ShrutixMusic.utils.database import add_served_chat, get_assistant, delete_served_chat


welcome_photo = "https://files.catbox.moe/ajobub.jpg"


@nand.on_message(filters.new_chat_members, group=-10)
async def join_watcher(client, message: Message):
    try:
        bot = await client.get_me() 
        chat = message.chat

        for member in message.new_chat_members:
            if member.id != bot.id:
                continue

            userbot = await get_assistant(chat.id)
            count = await client.get_chat_members_count(chat.id)
            username = chat.username

            invite_link = ""
            if not username:
                try:
                    link = await client.export_chat_invite_link(chat.id)
                    if link:
                        invite_link = f"\n𝐆ʀᴏᴜᴘ 𝐋ɪɴᴋ : {link}"
                except:
                    pass

            chat_username_text = f"@{username}" if username else "𝐏ʀɪᴠᴀᴛᴇ 𝐆ʀᴏᴜᴘ"

            msg = (
                f"✫ <b><u>𝐌ᴜsɪᴄ 𝐁ᴏᴛ 𝐀ᴅᴅᴇᴅ 𝐈ɴ 𝐍ᴇᴡ 𝐆ʀᴏᴜᴘ</u></b> ✫\n\n"
                f"𝐂ʜᴀᴛ 𝐍ᴀᴍᴇ : {chat.title}\n\n"
                f"𝐂ʜᴀᴛ 𝐈ᴅ : {chat.id}\n\n"
                f"𝐔sᴇʀɴᴀᴍᴇ : {chat_username_text}\n\n"
                f"𝐌ᴇᴍʙᴇʀs : {count}\n\n"
                f"𝐀ᴅᴅᴇᴅ 𝐁ʏ : {message.from_user.mention if message.from_user else '𝐔ɴᴋɴᴏᴡɴ'}"
                f"{invite_link}"
            )

            buttons = []
            if message.from_user:
                buttons.append(
                    [
                        InlineKeyboardButton(
                            "★ 𝐀ᴅᴅᴇᴅ 𝐁ʏ ★",
                            url=f"tg://openmessage?user_id={message.from_user.id}"
                        )
                    ]
                )

            await client.send_photo(
                LOGGER_ID,
                photo=welcome_photo,
                caption=msg,
                reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
            )

            await add_served_chat(chat.id)

            if username:
                try:
                    await userbot.join_chat(username)
                except:
                    pass

    except Exception as e:
        print(f"[Join_Watcher Error] {e}")



left_photos = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]


@nand.on_message(filters.left_chat_member, group=-12)
async def on_left_chat_member(client, message: Message):
    try:
        bot = await client.get_me()
        left = message.left_chat_member

        if not left or left.id != bot.id:
            return

        remove_by = message.from_user.mention if message.from_user else "𝐔ɴᴋɴᴏᴡɴ 𝐔sᴇʀ"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐂ʜᴀᴛ"
        chat_id = message.chat.id

        caption = (
            "✫ <b><u>#𝐋ᴇғᴛ_𝐆ʀᴏᴜᴘ</u></b> ✫\n\n"
            f"𝐂ʜᴀᴛ 𝐓ɪᴛʟᴇ : {title}\n\n"
            f"𝐂ʜᴀᴛ 𝐈ᴅ : {chat_id}\n\n"
            f"𝐔sᴇʀɴᴀᴍᴇ : {username}\n\n"
            f"𝐑ᴇᴍᴏᴠᴇᴅ 𝐁ʏ : {remove_by}\n\n"
            f"𝐁ᴏᴛ : @{bot.username}"
        )

        await client.send_photo(
            LOGGER_ID,
            photo=random.choice(left_photos),
            caption=caption
        )

        await delete_served_chat(chat_id)

        try:
            userbot = await get_assistant(chat_id)
            await userbot.leave_chat(chat_id)
        except:
            pass

    except Exception:
        pass
