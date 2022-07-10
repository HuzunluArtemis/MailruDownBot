# https://huzunluartemis.github.io/MailruDownBot/

from pyrogram import Client, filters
from bot import LOGGER, botStartTime
from config import Config
from pyrogram.types.messages_and_media.message import Message
import random
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
import requests
import heroku3
from helper_funcs.auth_user_check import AuthUserCheck
from helper_funcs.force_sub import ForceSub
from helper_funcs.progress import TimeFormatter, humanbytes

def getRandomUserAgent():
    agents = [
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.699.0 Safari/534.24",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.220 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (X11; CrOS i686 0.13.507) AppleWebKit/534.35 (KHTML, like Gecko) Chrome/13.0.763.0 Safari/534.35",
    "Mozilla/5.0 (X11; CrOS i686 0.13.587) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.14 Safari/535.1",
    "Mozilla/5.0 (X11; CrOS i686 1193.158.0) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7",
    "Mozilla/5.0 (X11; CrOS i686 12.0.742.91) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.93 Safari/534.30",
    "Mozilla/5.0 (X11; CrOS i686 12.433.109) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.93 Safari/534.30",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.04 Chromium/11.0.696.0 Chrome/11.0.696.0 Safari/534.24",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Ubuntu/10.10 Chromium/12.0.703.0 Chrome/12.0.703.0 Safari/534.24",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21",
    "Opera/9.80 (Windows NT 5.1; U; sk) Presto/2.5.22 Version/10.50",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
    "Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01",
    "Opera/9.80 (Windows NT 5.2; U; en) Presto/2.6.30 Version/10.63",
    "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51",
    "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.6.30 Version/10.61",
    "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01",
    "Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00",
    "Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01",
    "Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36"
    ]
    return agents[random.randint(0, len(agents)-1)]

def getHerokuDetails(h_api_key, h_app_name):
    if (not h_api_key) or (not h_app_name):
        LOGGER.info("if you want heroku dyno stats, read readme.")
        return None
    try:
        heroku_api = "https://api.heroku.com"
        Heroku = heroku3.from_key(h_api_key)
        app = Heroku.app(h_app_name)
        useragent = getRandomUserAgent()
        user_id = Heroku.account().id
        headers = {
            "User-Agent": useragent,
            "Authorization": f"Bearer {h_api_key}",
            "Accept": "application/vnd.heroku+json; version=3.account-quotas",
        }
        path = "/accounts/" + user_id + "/actions/get-quota"
        session = requests.Session()
        result = (session.get(heroku_api + path, headers=headers)).json()
        abc = ""
        account_quota = result["account_quota"]
        quota_used = result["quota_used"]
        quota_remain = account_quota - quota_used
        #abc += f"Full: {TimeFormatter(account_quota)} | "
        abc += f"<b>Dyno Used:</b> {TimeFormatter(quota_used*1000)} | "
        abc += f"<b>Free:</b> {TimeFormatter(quota_remain*1000)}\n"
        # App Quota
        AppQuotaUsed = 0
        OtherAppsUsage = 0
        for apps in result["apps"]:
            if str(apps.get("app_uuid")) == str(app.id):
                try:
                    AppQuotaUsed = apps.get("quota_used")
                except Exception as t:
                    LOGGER.error("error when adding main dyno")
                    LOGGER.error(t)
                    pass
            else:
                try:
                    OtherAppsUsage += int(apps.get("quota_used"))
                except Exception as t:
                    LOGGER.error("error when adding other dyno")
                    LOGGER.error(t)
                    pass
        LOGGER.info(f"This App: {str(app.name)}")
        abc += f"<b>This App:</b> {TimeFormatter(AppQuotaUsed*1000)}"
        abc += f" | <b>Other:</b> {TimeFormatter(OtherAppsUsage*1000)}"
        return abc
    except Exception as g:
        LOGGER.error(g)
        return None

@Client.on_message(filters.command("stats"))
def stats(_, message: Message):
    if not AuthUserCheck(message): return
    if ForceSub(message) == 400: return
    duz = message.reply_text("...")
    currentTime = TimeFormatter((time() - botStartTime)*1000)
    osUptime = TimeFormatter((time() - boot_time())*1000)
    total, used, free, disk= disk_usage('/')
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    sent = humanbytes(net_io_counters().bytes_sent)
    recv = humanbytes(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = humanbytes(swap.total)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = humanbytes(memory.total)
    mem_a = humanbytes(memory.available)
    mem_u = humanbytes(memory.used)
    stats = f'<b>Bot Uptime:</b> {currentTime}\n'\
            f'<b>OS Uptime:</b> {osUptime}\n'\
            f'<b>Total Disk Space:</b> {total}\n'\
            f'<b>Used:</b> {used} | <b>Free:</b> {free}\n'\
            f'<b>Upload:</b> {sent}\n'\
            f'<b>Download:</b> {recv}\n'\
            f'<b>CPU:</b> {cpuUsage}%\n'\
            f'<b>RAM:</b> {mem_p}%\n'\
            f'<b>DISK:</b> {disk}%\n'\
            f'<b>Physical Cores:</b> {p_core}\n'\
            f'<b>Total Cores:</b> {t_core}\n'\
            f'<b>SWAP:</b> {swap_t} | <b>Used:</b> {swap_p}%\n'\
            f'<b>Memory Total:</b> {mem_t}\n'\
            f'<b>Memory Free:</b> {mem_a}\n'\
            f'<b>Memory Used:</b> {mem_u}\n'
    heroku = getHerokuDetails(Config.HEROKU_API_KEY, Config.HEROKU_APP_NAME)
    if heroku: stats += heroku
    duz.edit_text(stats)
