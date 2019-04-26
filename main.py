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
# word2vec - read from https://habr.com/ru/post/429270/ and https://github.com/Myonin/silentio.su
# Проанализировать Вестник, Агрепаблик, Суртех, Хм., Мюсли, еще что-нибудь
#TODO: create folder with public id
#TODO: add examples

APP_NAME = "vk_public_analyzer"
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_BUILD = 0

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog=APP_NAME, 
        description='Tool for analyzing publics\' data from vk.com.')
    parser.add_argument('--path', type=str, help='Database path (default = data.db)')
    parser.add_argument('--clear_output', action='store_true', help='Clear output folder')
    parser.add_argument('--about', action='store_true', help='Show about info')
    return parser.parse_args()

def get_version():
    return "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_about_info():
    return ("\n" + APP_NAME + " " + get_version() + " Copyright (C) 2019 Yaroslav Zotov.\n" +
        "This program comes with ABSOLUTELY NO WARRANTY.\n" +
        "This is free software under MIT license; see the LICENSE file for copying conditions.")

if __name__ == '__main__':
    args = parse_args()
    if args.about:
        print(get_about_info())
        exit()
    if not os.path.isdir(OUTPUT_DIR):
        import nltk
        logging.info('Loading russian stopwords for NLTK')
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
    text_parse.get_topics(db)
    timing.drawplots(db)
