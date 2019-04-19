#!/bin/python3

import glob
import os

import argparse

import attachments
import common
import database
import text_parse
import timing
from common_data import *

#TODO:
# TODOlist
# word2vec
# some more from https://habr.com/ru/post/429270/ and https://github.com/Myonin/silentio.su
# Среднее просмотров-лайков-репостов за неделю/месяц/год/всегда
# Проанализировать Вестник, Агрепаблик, Суртех, Хм., Мюсли, еще что-нибудь
# TODO: replace print with logging
#TODO: create folder with public id

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog="vk_public_analyzer", 
        description='Tool fr analyzing public data from vk.com.')
    parser.add_argument('--path', type=str, help='Database path (default = data.db')
    parser.add_argument('--clear_output', action='store_true', help='Clear output folder')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if not os.path.isdir(OUTPUT_DIR):
        import nltk
        print('Loading russian stopwords for NLTK')
        nltk.download("stopwords")
        os.mkdir(OUTPUT_DIR)
    if args.clear_output: #clean output contents
        files = glob.glob('%s/*' % (OUTPUT_DIR))
        for f in files:
            os.remove(f)
    dbpath = args.path if args.path else DB_PATH
    db = database.DataBase(dbpath)
    common.common_data(db)
    common.alltop_data(db, 10)
    common.zero_data(db)
    common.authors_data(db)
    attachments.attachments_data(db)
    attachments.polls_info(db, 20)
    text_parse.popular_words(db, 200)
    timing.drawplots(db)
