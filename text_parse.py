
import random
import re
import string
import logging
from collections import Counter

from nltk.corpus import stopwords
from stop_words import get_stop_words
from pymystem3 import Mystem
from wordcloud import WordCloud
from gensim import corpora, models
logging.getLogger("gensim").setLevel(logging.ERROR)

import tabulate

from common_data import logging, OUTPUT_DIR

def preprocess_text(text):
    '''Convert text to tokens list'''
    mystem = Mystem() #Create lemmatizer
    russian_stopwords = stopwords.words("russian") #init stopwords list
    russian_stopwords.extend(get_stop_words('ru'))
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
        width=800, height=400).generate(words) #TODO: add stopwords
    image = wordcloud.to_image()
    image.save(output_path)

def popular_words(db, top_count):
    logging.info('Searching popular words...')
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

    logging.info('Drawing wordclouds')
    make_wordcloud(allwords_text, OUTPUT_DIR + 'allwords.png')
    make_wordcloud(word_data_to_text(top_words), OUTPUT_DIR + 'topwords.png')
    make_wordcloud(' '.join(get_hashtags(alltext)), OUTPUT_DIR + 'hashtags.png')
    logging.info('Done')

def get_themes(db):
    # https://github.com/Myonin/silentio.su/blob/master/topic_model_texts_lenta_ru.ipynb
    # https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/topic_modeling_Gensim.ipynb
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    alltext = db.select_all_text(2015) #TODO: process data by all years and maybe find more topics
    words_data = preprocess_text(alltext)
    words_data = [x for x in words_data if pattern.match(x)] #remove non-words
    if len(words_data) == 0:
        logging.warning("Empty dataset!")
        return
    text_data = [words_data]
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    # tfidf = models.TfidfModel(corpus)
    # corpus_tfidf = tfidf[corpus]
    data = models.ldamodel.LdaModel(corpus, id2word=dictionary,
        num_topics=1, passes=30)
    topics = data.print_topics(num_words=10)
    for topic in topics:
        print(topic)
