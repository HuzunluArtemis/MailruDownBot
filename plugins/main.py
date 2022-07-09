# https://huzunluartemis.github.io/MailruDownBot/

import shutil
import time
from pyrogram.types.messages_and_media.message import Message
from bot import LOGGER
from helper_funcs.absoluteFilePaths import absoluteFilePaths
from helper_funcs.force_sub import ForceSub
import os
import subprocess
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode

quee = []

def clear_downs():
    try: shutil.rmtree("downloads")
    except: pass
    if not os.path.isdir("downloads"): os.mkdir("downloads")

def run_task(message: Message, duzenlenecek: Message):
    try:
        clear_downs()
        duzenlenecek.edit_text("Downloading...")
        # download
        path = os.path.join(os.getcwd(), "downloads")
        cmd = f'python3 CloudMailruDL.py -d "{path}" {message.text}'
        LOGGER.info(cmd)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd="helper_funcs")
        stdout, stderr = proc.communicate()
        stderr = stderr.decode("utf-8")
        stdout = stdout.decode("utf-8")
        logstr = ""
        if stdout: logstr += "#stdout:\n\n" + stdout
        if stderr: logstr += "#stderr:\n\n" + stderr
        LOGGER.info(logstr)
        
        # upload
        inenler = list(absoluteFilePaths("downloads"))
        if len(inenler) != 1:
            duzenlenecek.edit_text("You can download only one file.")
        else:
            LOGGER.info(inenler[0])
            duzenlenecek.edit_text("Uploading...")
            message.reply_document(inenler[0],
                caption=f"[💚](https://huzunluartemis.github.io/MailruDownBot/) {os.path.basename(inenler[0])}",
                parse_mode=ParseMode.MARKDOWN, quote=True
            )
            duzenlenecek.edit_text("Finished.")
            time.sleep(10)
            duzenlenecek.delete()
    except Exception as e:
        LOGGER.exception(e)
    on_task_complete()

def on_task_complete():
    clear_downs()
    if len(quee) > 0:
        del quee[0]
    if len(quee) > 0:
        time.sleep(10)
        run_task(quee[0][0], quee[0][1])

@Client.on_message(filters.regex(r'\bhttps?://.*cloud\.mail\.ru\S+'))
def handler(client:Client, message: Message):
    if ForceSub(client, message) == 400: return
    duz = message.reply_text(f"`✔️ Your Turn: {len(quee)+1}`", quote=True)
    quee.append([message, duz])
    if len(quee) == 1: run_task(message, duz)

@Client.on_message(filters.command(["help", "yardım", "yardim", "start"]))
def welcome(client:Client, message: Message):
    if ForceSub(client, message) == 400: return
    te = "🇹🇷 Esenlikler. Bir mail.ru linki gönder ve sihrimi izle."
    te += "\n🇬🇧 Hi. Send me a mail.ru link and see my magic."
    message.reply_text(te)
