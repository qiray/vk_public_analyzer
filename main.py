#!/bin/python3

import os
import glob

import database
from common_data import *
import common
import attachments
import text_parse

#TODO:
# TODOlist
# best time for publications - graphics OR publications by days
# word, post, attachment count by time - graphics OR data by days
# word2vec
# some more from https://habr.com/ru/post/429270/ and https://github.com/Myonin/silentio.su
# Распределение просмотров-лайков-репостов по времени дня. Среднее за неделю/месяц/год/всегда
# Проанализировать Вестник, Агрепаблик, Суртех, Хм., Мюсли, еще что-нибудь

def dateposts(db):
    import datetime
    posts = db.get_posts_by_dates()
    times = sorted([datetime.datetime.fromtimestamp(int(x[0])).strftime('%H') for x in posts]) #hours
    print(times)

if __name__ == '__main__':
    if not os.path.isdir(OUTPUT_DIR):
        import nltk
        print('Loading russian stopwords for NLTK')
        nltk.download("stopwords")
        os.mkdir(OUTPUT_DIR)
    else: #folder exists so clean it's contents
        files = glob.glob('%s/*' % (OUTPUT_DIR))
        for f in files:
            os.remove(f)
    #TODO: get dbpath and count from args
    db = database.DataBase(DB_PATH)
    common.common_data(db)
    common.alltop_data(db, 10)
    common.zero_data(db)
    common.authors_data(db)
    attachments.attachments_data(db)
    attachments.polls_info(db, 20)
    text_parse.popular_words(db, 200)
    # dateposts(db)
