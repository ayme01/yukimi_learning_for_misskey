import random
import MeCab
from logging import getLogger

def change_yukimi(text):
    logger = getLogger(__name__)
    tagger = MeCab.Tagger()
    if random.randint(0, 3) == 0:
        analyzed_tweets = ["…"] * random.randint(1, 4) # 文頭に25%の確率で三点リーダを付ける
    else:
        analyzed_tweets = []
    node = tagger.parseToNode(text)

    logger.info(node)
    while node:
        part_of_speech = ''
        analyzed_tweets.append(node.surface)
        for block in node.feature:
            part_of_speech += block
            if block == '詞':
                break
        if part_of_speech == '副詞' or part_of_speech == '助詞': # 文章の区切りに25%で三点リーダを付ける
            analyzed_tweets.append("…" * random.randint(1, 4))

        node = node.next

    if random.randint(0, 7) == 0:
        analyzed_tweets.append("…" * random.randint(1, 4) + "ふふ" + "…" * random.randint(1, 4))

    logger.info("".join(analyzed_tweets))
    return "".join(analyzed_tweets)
