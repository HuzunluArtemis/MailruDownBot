# https://huzunluartemis.github.io/MailruDownBot/

import json
import shutil
import time
from pyrogram.types.messages_and_media.message import Message
from bot import LOGGER
from config import Config
from helper_funcs.absoluteFilePaths import absoluteFilePaths
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
import os
import subprocess
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from os import popen
from helper_funcs.progress import humanbytes, progress_for_pyrogram

# aria2 = get_aria2()
quee = []

def clear_downs():
    try: shutil.rmtree("downloads")
    except: pass
    if not os.path.isdir("downloads"): os.mkdir("downloads")

def run_task(message: Message, duzenlenecek: Message):
    try:
        # parse data from link
        command = f'python helper_funcs/CloudMailruDL.py -s {message.text}'
        result = popen(command).read()
        result = result.splitlines()[-1]
        data = json.loads(result)
        
        dl_url = data['download']
        file_size = int(data['file_size'])
        file_name = data['file_name']

        # log
        if Config.LOG_CHANNEL:
            try:
                message._client.send_message(
                    Config.LOG_CHANNEL,
                    f"#NewDownload\n\nUser: {message.from_user.mention}\n" +
                    f"User ID: `{message.from_user.id}`\nLink: {message.text}" +
                    f"\nFilesize: {humanbytes(file_size)} ({file_size} bytes)\nFilename: `{file_name}`"
            ) 
            except Exception as e:
                LOGGER.exception(e)
        
        # check filesize
        if file_size > Config.MAX_FILESIZE:
            duzenlenecek.edit_text(f"Size limit: {humanbytes(Config.MAX_FILESIZE)} ({str(Config.MAX_FILESIZE)} bytes)")
            return on_task_complete()

        # download
        clear_downs()
        duzenlenecek.edit_text("Downloading...")
        path = os.path.join(os.getcwd(), "downloads")
        if Config.USE_ARIA2:
        # download = aria2.add_uris([dl_url], {'dir': path}) ?
            cmd = f'aria2c --split=10 --min-split-size=10M --max-connection-per-server=10 --daemon=false --allow-overwrite=true -d "{path}" -o "{file_name}" "{dl_url}"'
        else:
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
        
        # control
        inenler = list(absoluteFilePaths("downloads"))
        if len(inenler) != 1:
            duzenlenecek.edit_text("You can download only one file.")
        else:
            LOGGER.info(inenler[0])
            s_time = time.time()
            
            # thumb
            thumb = os.path.join("thumbnails", str(message.from_user.id) + ".jpg")
            if not os.path.isfile(thumb): thumb = None

            # upload
            message.reply_document(inenler[0],
                caption=f"[💚](https://huzunluartemis.github.io/MailruDownBot/) {os.path.basename(inenler[0])}",
                parse_mode=ParseMode.MARKDOWN, quote=True, progress=progress_for_pyrogram,
                progress_args=(f"Uploading: `{file_name}`",  duzenlenecek, s_time), force_document=Config.FORCE_DOC_UPLOAD,
                thumb=thumb
            )
            duzenlenecek.edit_text("Finished.")
            time.sleep(10)
            duzenlenecek.delete()
    except json.decoder.JSONDecodeError as e:
        duzenlenecek.edit_text("Cant extract the link. Try again later.")
        LOGGER.exception(e)
    except Exception as e:
        duzenlenecek.edit_text("Cannot download. Try again later.")
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
    if not AuthUserCheck(message): return
    if ForceSub(client, message) == 400: return
    # add to quee
    duz = message.reply_text(f"✅ Your Turn: {len(quee)+1}\nWait. Dont spam with same link.", quote=True)
    quee.append([message, duz])
    if len(quee) == 1: run_task(message, duz)

@Client.on_message(filters.command(["help", "yardım", "yardim", "start"]))
def welcome(client:Client, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(client, message) == 400: return
    te = "🇹🇷 Esenlikler. Bir mail.ru linki gönder ve sihrimi izle."
    te += "\n🇬🇧 Hi. Send me a mail.ru link and see my magic."
    te += "\n\nSet Thumbnail? Here: /save /clear /show"
    message.reply_text(te)
