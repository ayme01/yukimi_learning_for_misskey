# 1つ上のディレクトリの絶対パスを取得し、sys.pathに登録する
import sys
from os.path import dirname
parent_dir = dirname(dirname(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir) 

import re
from collections import deque
from ngword_filter import judgement_sentence
import random
from misskey import Misskey
import json
import requests
from logging import getLogger
import time

with open('../config.json', 'r') as json_file:
    config = json.load(json_file)

#Misskey.py API
misskey = Misskey(config['token']['server'], i= config['token']['i'])

#Misskey API json request用
get_tl_url = "https://" + config['token']['server'] + "/api/notes/timeline"
limit = 10
get_tl_json_data = {
    "i" : config["token"]["i"],
    "limit": limit,
}

def sub_function(text):
    patterns = [
        r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+',
        r'@.*',
        r'#.*',
        r"<[^>]*?>",
        r"\(.*"
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text)
    return text

def replace_function(text):
    replacements = {
        '\\': "",
        '*': "",
        '\n': "",
        '\u3000': "",
        '俺': "私",
        '僕': "私",
        ' ': ""
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text



def get_tl_misskey():
    logger = getLogger(__name__)
    response = requests.post(
        get_tl_url,
        json.dumps(get_tl_json_data),
        headers={'Content-Type': 'application/json'})
    hash = response.json()
    choice_note = random.choice(hash)
    choice_id = str(choice_note["id"]) 
    choice_text = str(choice_note["text"])
    line = sub_function(choice_text)
    line = replace_function(line)
    mfm_judge = list(line)
    for one_letter in mfm_judge:
        if(one_letter == '$'):
            return "None"
    try:
        if choice_note['reactions']['❤'] == 1:
            return "None"
    except KeyError:
        #自分自身の投稿を除外
        if choice_note["user"]["username"] == "YukimiLearning" or choice_note['cw'] != None:
            return "None"
        #フォロワー限定投稿を除外
        elif choice_note["visibility"] == "followers":
            return "None"
        #センシティブワード検知
        elif judgement_sentence(line) != True and line != "None" and line != "":
            try:
                misskey.notes_reactions_create(choice_id,"❤️")
            except:
                time.sleep(1200)
                return "None"
            logger.info(line)
            return(line)
        else:
            return "None"
    
# print(get_tl_misskey())