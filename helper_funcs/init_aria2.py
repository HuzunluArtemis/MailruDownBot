import subprocess
import threading
import aria2p
from bot import LOGGER
# created for this repo https://huzunluartemis.github.io/MailruDownBot/
# not used.

def init_aria2():
    # start the daemon, aria2c command
    aria2_daemon_start_cmd = ["aria2c"]
    aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--max-connection-per-server=10")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=false")
    aria2_daemon_start_cmd.append("--rpc-listen-port=6800")
    aria2_daemon_start_cmd.append("--split=10")
    #
    proc = subprocess.Popen(aria2_daemon_start_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = proc.communicate()
    stderr = stderr.decode("utf-8")
    stdout = stdout.decode("utf-8")
    logstr = ""
    if stdout: logstr += "#stdout:\n\n" + stdout
    if stderr: logstr += "#stderr:\n\n" + stderr
    LOGGER.info(logstr)
    
    LOGGER.info("aria2 started.")
    
def get_aria2():
    # init aria2 +
    initing_aria2 = threading.Thread(target=init_aria2, name="Downloader")
    initing_aria2.start()
    # init aria2 -
    return aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port="6800",
        secret=""
    )
    )