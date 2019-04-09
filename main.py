#!/bin/python3

import os
import glob
import random
import re
import string
import statistics
from collections import Counter

from nltk.corpus import stopwords
from pymystem3 import Mystem
from wordcloud import WordCloud
import tabulate

import database

#TODO:
# TODOlist
# best authors (top 10-20) - posts count and likes, reposts
# best time for publications - graphics
# word, post, attachment count by time - graphics
# top polls - users count
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

def popular_words(db, top_count):
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    alltext = db.select_all_text() #whole plain text
    words_data = preprocess_text(alltext) #list of preprocessed words
    allwords_text = ' '.join(words_data) #text with preprocessed words
    words_data = [x for x in words_data if pattern.match(x)] #remove non-words
    sorted_words_data = sorted(Counter(words_data).items(), key=lambda kv: kv[1], reverse=True)
    top_words = sorted_words_data[:top_count] #list of tuples of top words

    f = open(OUTPUT_DIR + "top_words.csv","w")
    f.write('Word;Count\n')
    headers = ['Word', 'Count']
    print("\nTop words:")
    table_values = []
    for word in top_words:
        f.write('%s;%d\n' % (word[0], word[1]))
        table_values.append(word)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, numalign="right"))

    make_wordcloud(allwords_text, OUTPUT_DIR + 'allwords.png')
    make_wordcloud(word_data_to_text(top_words), OUTPUT_DIR + 'topwords.png')
    make_wordcloud(' '.join(get_hashtags(alltext)), OUTPUT_DIR + 'hashtags.png')

def common_data_row(data_values, value, name, count, csvfile):
    try:
        mode = statistics.mode(data_values)
    except:
        print("[Warning] %s doesn't have unique mode" % (name))
        mode = 0
    values = [name, value, value/count, statistics.median(data_values), mode,
        statistics.stdev(data_values)]
    csvfile.write('%s;%d;%.4g;%.4g;%.4g;%.4g\n' % (values[0], values[1], values[2], values[3],
        values[4], values[5]))
    return values

def common_data(db):
    data, names, columns = db.get_common_data()
    f = open(OUTPUT_DIR + "common.csv","w")
    headers = ['Parameter', 'Count', 'Average (Mean)', 'Median', 'Mode', 'Stdev']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\nCommon data:")
    count = data[0]
    column_count = 0
    table_values = []
    for i, value in enumerate(data):
        if i > 0 and column_count < len(columns):
            table_values.append(common_data_row(db.get_column_data(columns[column_count]),
                value, names[i], count, f))
            column_count += 1
        else:
            values = [names[i], value]
            f.write('%s;%d\n' % (values[0], values[1]))
            table_values.append(values)

    data_values = db.get_texts_length()
    table_values.append(common_data_row(data_values, sum(data_values), "Text", count, f))

    f.close()
    print(tabulate.tabulate(table_values, headers=headers, floatfmt=".4g", numalign="right"))

def top_data(name, max_values, min_values):
    '''Show top data'''
    f = open(OUTPUT_DIR + "extremum_%s.csv" % (name),"w")
    headers = ['id', 'Max', 'id', 'Min']
    if not min_values:
        headers = ['id', 'Max']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\n%s extremum data:" % (name))
    table_values = []
    for i in range(len(max_values)):
        if min_values:
            values = [max_values[i][1], max_values[i][0], min_values[i][1], min_values[i][0]]
            f.write('%d;%d;%d;%d\n' % (values[0], values[1], values[2], values[3]))
        else:
            values = [max_values[i][1], max_values[i][0]]
            f.write('%d;%d;\n' % (values[0], values[1]))
        table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, numalign="right"))

def alltop_data(db, top_count):
    names = ('Likes', 'Reposts', 'Comments', 'Views', 'Attachments')
    columns = ('likes_count', 'reposts_count', 'comments_count', 'views_count', 
        'attachments_count')
    for i in range(len(names)):
        top_data(names[i], db.get_top_data(columns[i], top_count), None)
    top_data('Text', db.get_top_texts(top_count), None)

def zero_data(db):
    names = ('Likes', 'Reposts', 'Comments', 'Attachments')
    columns = ('likes_count', 'reposts_count', 'comments_count', 'attachments_count')
    f = open(OUTPUT_DIR + "zeros.csv", "w")
    headers = ['Parameter', 'Count']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\nPosts without:")
    table_values = []
    for i in range(len(names)):
        values = [names[i], db.get_zero_data(columns[i])]
        f.write('%s;%d\n' % (values[0], values[1]))
        table_values.append(values)
    values = ['Text', db.get_zero_texts()]
    f.write('%s;%d\n' % (values[0], values[1]))
    table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, numalign="right"))

def attachments_data(db):
    data, names = db.get_attachments_types()
    f = open(OUTPUT_DIR + "attachments.csv","w")
    headers = ['Parameter', 'Count']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\nAttachments data:")
    table_values = []
    for i, value in enumerate(data):
        values = [names[i], value[1]]
        f.write('%s;%d\n' % (values[0], values[1]))
        table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, floatfmt=".4g", numalign="right"))

def common_authors_data(db): #TODO: add info about reposts
    data = db.get_posts_by_authors()
    f = open(OUTPUT_DIR + "authors.csv","w")
    headers = ['Author id', 'Posts count', 'Likes count', 'Average likes', 'Median likes']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\nAuthors data:")
    table_values = []
    for i, _ in enumerate(data):
        posts = db.get_posts_by_author(data[i][0])
        posts_likes = [x[0] for x in posts]
        values = [data[i][0], data[i][1], data[i][2], data[i][2]/data[i][1], statistics.median(posts_likes)]
        f.write('%d;%d;%d;%.4g;%.4g\n' % (values[0], values[1], values[2], values[3], values[4]))
        table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, floatfmt=".4g", numalign="right"))

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
    common_data(db)
    alltop_data(db, 10)
    zero_data(db)
    attachments_data(db)
    popular_words(db, 200)
    common_authors_data(db)
