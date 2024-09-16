### main.py
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from Misskey.follow_back import follow_back
from Misskey.get_timeline import get_tl_misskey
from Misskey.note import note
from yukimi_text.yukimi_text import change_yukimi
import logging

logging.basicConfig(level=logging.DEBUG)


sched = BlockingScheduler()
class Config(object):
    SCHEDULER_API_ENABLED = True

@sched.scheduled_job('cron', id='note', minute='*/10')
def cron_note():
    text = get_tl_misskey()
    while text == "None" or text == '':
        time.sleep(120)
        text = get_tl_misskey()
    post_word = change_yukimi(text)
    note(post_word)

@sched.scheduled_job('cron', id='follow_back', minute='*/59')
def cron_follow_back():
    follow_back()

if __name__ == "__main__":
    sched.start()
