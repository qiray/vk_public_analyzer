#!/bin/python3

import os
import random
import re
import string
import statistics
from collections import Counter

from nltk.corpus import stopwords
from pymystem3 import Mystem
from wordcloud import WordCloud

import database

#TODO:
# TODOlist
# mediana, moda and expected value for likes, comments, views, reposts, attachments and ratio.
# most likes, comments, views, reposts, attachments.
# average and top attachments
# top attachments - images, video, URLs or audio
# best authors - posts count and likes, reposts
# best time for publications - graphics
# word, post, attachment count by time - graphics
# top polls
# word2vec
# some more from https://habr.com/ru/post/429270/
# Проанализировать Вестник, Агрепаблик, Суртех, Хм., Мюсли, еще что-нибудь

OUTPUT_DIR = "output/"
DB_PATH = "data.db"

def preprocess_text(text):
    '''Convert text to tokens list'''
    mystem = Mystem() #Create lemmatizer
    russian_stopwords = stopwords.words("russian") #init stopwords list
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords\
        and token != " " and token.strip() not in string.punctuation]
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
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    alltext = database.select_all_text(dbpath) #whole plain text
    words_data = preprocess_text(alltext) #list of preprocessed words
    allwords_text = ' '.join(words_data) #text with preprocessed words
    words_data = [x for x in words_data if pattern.match(x)] #remove non-words
    sorted_words_data = sorted(Counter(words_data).items(), key=lambda kv: kv[1], reverse=True)
    top_words = sorted_words_data[:top_count] #list of tuples of top words

    f = open(OUTPUT_DIR + "top_words.csv","w")
    f.write('Word;Count\n')
    print("\nTop words:")
    for word in top_words:
        f.write('%s;%d\n' % (word[0], word[1]))
        print(word[0], "=", word[1])
    f.close()

    make_wordcloud(allwords_text, OUTPUT_DIR + 'allwords.png')
    make_wordcloud(word_data_to_text(top_words), OUTPUT_DIR + 'topwords.png')
    make_wordcloud(' '.join(get_hashtags(alltext)), OUTPUT_DIR + 'hashtags.png')

def common_data(dbpath):
    data, names = database.get_common_data(dbpath)
    f = open(OUTPUT_DIR + "common.csv","w")
    f.write('Parameter;Count;Average\n')
    print("\nCommon data:")
    count = data[0]
    for i, value in enumerate(data):
        f.write('%s;%d;%.4f\n' % (names[i], value, value/count))
        print('%s = %d (%.4g)' % (names[i], value, value/count))
    f.close()

if __name__ == '__main__':
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    #TODO: get dbpath and count from args
    common_data(DB_PATH)
    popular_words(DB_PATH, 200)

    #TODO: use it instead of common_data?
    # likes = database.get_column_data(DB_PATH, 'likes_count')
    # print(statistics.median(likes))
    # print(statistics.mode(likes))
    # print(statistics.mean(likes))
    # print(statistics.stdev(likes))

