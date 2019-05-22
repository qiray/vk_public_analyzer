
import random
import re
import string
from collections import Counter

import tabulate
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from stop_words import get_stop_words
from pymystem3 import Mystem
from wordcloud import WordCloud
from gensim import corpora, models

from common_info import print_info, get_output_path

russian_stopwords = stopwords.words("russian") #init stopwords list
russian_stopwords.extend(get_stop_words('ru')) #update stopwords list

# Some useful URLs
# https://habr.com/ru/post/429270/ and https://github.com/Myonin/silentio.su
# https://github.com/Myonin/silentio.su/blob/master/topic_model_texts_lenta_ru.ipynb
# https://github.com/susanli2016/Machine-Learning-with-Python/blob/master/topic_modeling_Gensim.ipynb

def preprocess_text(text):
    '''Convert text to tokens list'''
    mystem = Mystem() #Create lemmatizer
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
    if len(words) == 0:
        print_info("Warning! No data for wordcloud")
        return
    wordcloud = WordCloud(background_color="#FFFFFF",
        width=800, height=400, stopwords=['это']).generate(words)
    image = wordcloud.to_image()
    image.save(output_path)

def popular_words(db, top_count):
    print_info('Searching popular words...')
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    alltext = db.select_all_text() #whole plain text
    words_data = preprocess_text(alltext) #list of preprocessed words
    allwords_text = ' '.join(words_data) #text with preprocessed words
    words_data = [x for x in words_data if pattern.match(x)] #remove non-words
    sorted_words_data = sorted(Counter(words_data).items(), key=lambda kv: kv[1], reverse=True)
    top_words = sorted_words_data[:top_count] #list of tuples of top words

    f = open(get_output_path() + "top_words.csv","w", encoding="utf-8")
    f.write('Word;Count\n')
    headers = ['Word', 'Count']
    print("\nTop words:")
    table_values = []
    for word in top_words:
        f.write('%s;%d\n' % (word[0], word[1]))
        table_values.append(word)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, numalign="right"))

    print_info('Drawing wordclouds')
    make_wordcloud(allwords_text, get_output_path() + 'allwords.png')
    make_wordcloud(word_data_to_text(top_words), get_output_path() + 'topwords.png')
    make_wordcloud(' '.join(get_hashtags(alltext)), get_output_path() + 'hashtags.png')
    print_info('Done')

def get_topics(db):
    for i in db.get_posts_year_range():
        get_topic_by_year(db, i)
    get_topic_by_year(db)

def topics_plot(topic_names, topic_data, name):
    plt.rcdefaults()
    _, ax = plt.subplots()
    plt.subplots_adjust(right=0.9, left=0.2)

    y_pos = [i for i in range(len(topic_names))]
    ax.barh(y_pos, topic_data, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(topic_names)
    ax.invert_yaxis()
    ax.set_xlabel('Weight')
    ax.set_title('Topics')

    plt.savefig(name)
    plt.close()

def get_topic_by_year(db, year=None):
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    alltext = db.select_all_text(year)
    words_data = preprocess_text(alltext)
    words_data = [x for x in words_data if pattern.match(x)] #remove non-words
    if len(words_data) == 0:
        print_info("Empty dataset!")
        return
    text_data = [words_data]
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    data = models.ldamodel.LdaModel(corpus, id2word=dictionary,
        num_topics=1, passes=30)
    topics = data.print_topics(num_words=10)
    if year:
        print_info("Topics for %d" % year)
        name = get_output_path() + "topics_%d" % year
    else:
        print_info("Common topics")
        name = get_output_path() + "topics"
    f = open(name + ".csv", "w", encoding="utf-8")
    f.write('Weight;Word\n')
    topic_names = []
    topic_data = []
    for topic in topics:
        topic_words = topic[1].split('+')
        for i in topic_words:
            result = i.replace(" ", "")
            result = result.replace("\"", "")
            values = result.split('*')
            topic_data.append(float(values[0]))
            topic_names.append(values[1])
            f.write('%s;%s\n' % (values[0], values[1]))
        print(topic[1])
    f.close()
    topics_plot(topic_names, topic_data, name + ".png")
