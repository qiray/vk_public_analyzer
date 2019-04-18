#!/bin/python3

import os
import glob

import database
from common_data import *
import common
import attachments
import text_parse
import timing

#TODO:
# TODOlist
# word2vec
# some more from https://habr.com/ru/post/429270/ and https://github.com/Myonin/silentio.su
# Среднее просмотров-лайков-репостов за неделю/месяц/год/всегда
# Проанализировать Вестник, Агрепаблик, Суртех, Хм., Мюсли, еще что-нибудь

if __name__ == '__main__':
    if not os.path.isdir(OUTPUT_DIR):
        import nltk
        print('Loading russian stopwords for NLTK')
        nltk.download("stopwords")
        os.mkdir(OUTPUT_DIR)
    else: #folder exists so clean it's contents
        files = glob.glob('%s/*' % (OUTPUT_DIR)) #TODO: clean flag from args
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
    timing.drawplots(db)
