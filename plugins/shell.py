# https://huzunluartemis.github.io/MailruDownBot/

from pyrogram import Client, filters
from bot import LOGGER
from config import Config
import subprocess
from pyrogram.types.messages_and_media.message import Message

@Client.on_message(filters.command("shell"))
def shell(_, message:Message):
    if Config.OWNER_ID == 0 or message.from_user.id != Config.OWNER_ID: return
    try:
        cmd = message.text.split(' ', 1)
        if len(cmd) == 1:
            return message.reply_text('🇬🇧 No command to execute was given.\n\n🇹🇷 Boşluk bırakıp komut gir zırcahil seni.',
                reply_to_message_id = message.id)
        cmd = cmd[1]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        reply = ''
        stderr = stderr.decode()
        stdout = stdout.decode()
        if stdout:
            reply += f"Stdout:\n`{stdout}`\n"
            LOGGER.info(f"Shell - {cmd} - {stdout}")
        if stderr:
            reply += f"Stderr:\n`{stderr}`\n"
            LOGGER.error(f"Shell - {cmd} - {stderr}")
        if len(reply) > 3000:
            with open('shell.txt', 'w') as file:
                file.write(reply)
            with open('shell.txt', 'rb') as doc:
                message.reply_document(
                    document=doc,
                    filename=doc.name
                )
        else:
            message.reply_text(reply)
    except:
        message.reply_text("🇬🇧 Maybe your shell message was empty.\n🇹🇷 Boş bir şeyler döndü valla.\n\n"+ reply,
                reply_to_message_id = message.id)
