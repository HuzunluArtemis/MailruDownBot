from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from config import Config

@Client.on_message(filters.command("log"))
def log(_, message:Message):
    if Config.OWNER_ID == 0 or message.from_user.id != Config.OWNER_ID: return
    message.reply_document("log.txt")
