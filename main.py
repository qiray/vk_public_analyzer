#!/bin/python3

import glob
import os
import sys
import traceback

import argparse
import nltk

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

import attachments
import common
import database
import text_parse
import timing
from common_info import get_output_path, set_output_path, print_info

DB_PATH = "data.db"

#TODO: add example article

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
    try:
        args = parse_args()
        if args.about:
            print(get_about_info())
            exit()
        dbpath = args.path if args.path else DB_PATH
        db = database.DataBase(dbpath)
        public_id = db.get_public_id()
        set_output_path('%s/%s/' % (get_output_path(), public_id))
        if not os.path.isdir(get_output_path()):
            os.makedirs(get_output_path())
        if args.clear_output: #clean output contents
            files = glob.glob('%s/*' % (get_output_path()))
            for f in files:
                os.remove(f)
        common.common_data(db)
        common.alltop_data(db, 10)
        common.zero_data(db)
        common.authors_data(db)
        attachments.attachments_data(db)
        attachments.polls_info(db, 20)
        text_parse.popular_words(db, 200)
        text_parse.get_topics(db)
        timing.drawplots(db)
    except BaseException as e:
        print(e)
        traceback.print_exc()
        exit(1)
