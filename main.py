#!/bin/python3

from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from collections import Counter

import database

#TODO:
# TODOlist
# word and tag cloud - https://www.datacamp.com/community/tutorials/wordcloud-python
# common data - posts, likes, reposts, comments, views, attachmens, ads etc.
# most and average likes, comments, views, reposts and ratio
# average and top attachments
# best authors - posts count and likes, reposts
# best time for publications - graphics
# word, post, attachment count by time - graphics
# top polls
# top attachments - images, video, URLs or audio
# word2vec
# some more from https://habr.com/ru/post/429270/
# csv and images output
# Проанализировать Вестник, Агрепаблик, Суртех, Хм., Мюсли, еще что-нибудь

def preprocess_text(text, russian_stopwords):
    '''Convert text to tokens list'''
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
        and token != " " and token.strip() not in punctuation]
    return tokens

if __name__ == '__main__':
    mystem = Mystem() #Create lemmatizer 
    russian_stopwords = stopwords.words("russian") #init stopwords list
    alltext = database.select_all_text("data.db") #TODO: get dbpath from args
    words_data = Counter(preprocess_text(alltext, russian_stopwords))
    sorted_words_data = sorted(words_data.items(), key=lambda kv: kv[1], reverse=True)
    print(sorted_words_data[:50])
