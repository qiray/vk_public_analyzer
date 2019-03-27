#!/bin/python3

import os
import random
import re
from collections import Counter
from string import punctuation

from nltk.corpus import stopwords
from pymystem3 import Mystem
from wordcloud import WordCloud

import database

#TODO:
# TODOlist
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

OUTPUT_DIR = "output/"

def preprocess_text(text):
    '''Convert text to tokens list'''
    mystem = Mystem() #Create lemmatizer
    russian_stopwords = stopwords.words("russian") #init stopwords list
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
        and token != " " and token.strip() not in punctuation]
    return tokens

def get_hashtags(text):
    result = re.findall(r'#\w+', text)
    random.shuffle(result)
    return result

def word_data_to_text(word_data):
    '''Convert list of tuples (word, count) to shuffled text'''
    result = []
    for v in word_data:
        result.extend([v[0]] * v[1])
    random.shuffle(result)
    return ' '.join(result)

def make_wordcloud(words, output_path):
    wordcloud = WordCloud(background_color="#FFFFFF", 
        width=800, height=400).generate(words)
    image = wordcloud.to_image()
    image.save(output_path)

def popular_words(dbpath, top_count):
    alltext = database.select_all_text(dbpath) #whole plain text
    words_data = preprocess_text(alltext) #list of preprocessed words
    allwords_text = ' '.join(words_data) #text with preprocessed words
    sorted_words_data = sorted(Counter(words_data).items(), key=lambda kv: kv[1], reverse=True)
    top_words = sorted_words_data[:top_count] #list of tuples of top words

    f = open(OUTPUT_DIR + "top_words.csv","w")
    f.write('Word;Count\n')
    for word in top_words:
        f.write('%s;%d\n' % (word[0], word[1]))
    f.close()

    make_wordcloud(allwords_text, OUTPUT_DIR + 'allwords.png')
    make_wordcloud(word_data_to_text(top_words), OUTPUT_DIR + 'topwords.png')
    make_wordcloud(' '.join(get_hashtags(alltext)), OUTPUT_DIR + 'hashtags.png')

if __name__ == '__main__':
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    database.get_common_data("data.db")
    popular_words("data.db", 200) #TODO: get dbpath and count from args

