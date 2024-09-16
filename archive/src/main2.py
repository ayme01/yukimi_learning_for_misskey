from apscheduler.schedulers.blocking import BlockingScheduler
import time
from Misskey.follow_back import follow_back
from Misskey.get_timeline import get_tl_misskey
from Misskey.note import note
from yukimi_text.yukimi_text import change_yukimi
import logging
from rich.logging import RichHandler
import threading
import time

# ロガーの設定
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True,rich_tracebacks=True)]
)

logging.basicConfig(
    level=logging.ERROR,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True,rich_tracebacks=True)]
)

logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True,rich_tracebacks=True)]
)

logging.basicConfig(
    level=logging.CRITICAL,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True,rich_tracebacks=True)]
)

def cron_note():
    while True:
        text = get_tl_misskey()
        while text == "None" or text == '':
            time.sleep(120)
            text = get_tl_misskey()
        post_word = change_yukimi(text)
        note(post_word)
        time.sleep(600)

def cron_follow_back():
    while True:
        follow_back()
        time.sleep(3600)

if __name__ == "__main__":
    thread_1 = threading.Thread(target=cron_note)
    thread_2 = threading.Thread(target=cron_follow_back)

    thread_2.start()
    thread_1.start()

