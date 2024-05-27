# 1つ上のディレクトリの絶対パスを取得し、sys.pathに登録する
import sys
import os
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

misskey = Misskey(os.environ['SERVER'], i=os.environ['TOKEN'])

#Misskey API json request用
get_tl_url = "https://" + os.environ['SERVER'] + "/api/notes/timeline"
limit = 30
get_tl_json_data = {
    "i" : os.environ['TOKEN'],
    "limit": limit,
}


# ToDo:この部分をmfm-jsでデコードするようにする
def get_tl_misskey():
    response = requests.post(
        get_tl_url,
        json.dumps(get_tl_json_data),
        headers={'Content-Type': 'application/json'})
    hash = response.json()
    choice_note = random.choice(hash)
    choice_id = str(choice_note["id"]) 
    choice_text = str(choice_note["text"])
    ###
    #URLその他もろもろ除外
    # Todo 
    #とりあえずいらんもの除外しまくったので後で整理
    #
    ###
    line = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", choice_text)
    line = re.sub(r'@.*', "", line)
    line = re.sub(r'#.*', "", line)
    line = re.sub(r"<[^>]*?>", "", line)
    line = re.sub(r"\(.*", "", line)
    line = line.replace('\\', "")
    line = line.replace('*', "")
    line = line.replace('\n', "")
    line = line.replace('\u3000', "")
    line = line.replace('俺', "私")
    line = line.replace('僕', "私")
    line = line.replace(' ', "")
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
            misskey.notes_reactions_create(choice_id,"❤️")
            return(line)
        else:
            return "None"
    
# print(get_tl_misskey())