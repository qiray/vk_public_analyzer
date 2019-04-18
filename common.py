
import statistics
from collections import Counter

import tabulate

from common_data import OUTPUT_DIR

def common_data_row(data_values, value, name, count, csvfile):
    try:
        mode = statistics.mode(data_values)
    except:
        c = Counter(data_values)
        mode = c.most_common(1)[0][0]
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
    headers = ['Post id', 'Max', 'Author id', 'Post id', 'Min', 'Author id']
    if not min_values:
        headers = ['Post id', 'Max', 'Author id']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\n%s extremum data:" % (name))
    table_values = []
    for i in range(len(max_values)):
        if min_values:
            values = [max_values[i][1], max_values[i][0], max_values[i][2],
                min_values[i][1], min_values[i][0], min_values[i][2]]
            f.write('%d;%d;%d;%d;%d;%d\n' % (values[0], values[1], values[2],
                values[3], values[4], values[5]))
        else:
            values = [max_values[i][1], max_values[i][0], max_values[i][2]]
            f.write('%d;%d;%d\n' % (values[0], values[1], values[2]))
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

def authors_data(db):
    data = db.get_posts_by_authors()
    f = open(OUTPUT_DIR + "authors.csv","w")
    headers = ['Author id', 'Posts', 'Likes', 'Reposts', 'Comments', 
        'Views', 'Attachments', 'Text length']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\nAuthors data:")
    table_values = []
    for i, _ in enumerate(data):
        values = [data[i][0], data[i][1], data[i][2], data[i][3],
            data[i][4], data[i][5], data[i][6], data[i][7]]
        f.write('%d;%d;%d;%d;%d;%d;%d;%d\n' % (values[0], values[1], values[2],
            values[3], values[4], values[5], values[6], values[7]))
        if i <= 20: #Show only top 20 authors
            table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, floatfmt=".4g", numalign="right"))
