import statistics
from collections import Counter

import tabulate

from common_data import OUTPUT_DIR

def attachments_data(db):
    data = db.get_attachments_types()
    f = open(OUTPUT_DIR + "attachments.csv","w", encoding="utf-8")
    headers = ['Parameter', 'Count']
    header = ";".join(headers)
    f.write(header + '\n')
    print("\nAttachments data:")
    table_values = []
    for value in data:
        values = [db.get_attachments_name(value[0]), value[1]]
        f.write('%s;%d\n' % (values[0], values[1]))
        table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, floatfmt=".4g", numalign="right"))

def polls_info(db, count):
    polls = db.get_polls()
    votes = [int(x[6]) for x in polls]
    length = len(votes)
    total_votes = sum(votes)
    average = total_votes/length
    try:
        mode = statistics.mode(votes)
    except:
        c = Counter(votes)
        mode = c.most_common(1)[0][0]
    headers = ['Parameter', 'Count', 'Total votes', 'Average (Mean)', 'Median', 'Mode', 'Stdev']
    values = ['Polls', length, total_votes, average, statistics.median(votes), mode, 
        statistics.stdev(votes)]
    print("\nPolls data:")
    print(tabulate.tabulate([values], headers=headers, floatfmt=".4g", numalign="right"))
    f = open(OUTPUT_DIR + "common_polls.csv","w", encoding="utf-8")
    f.write(";".join(headers) + '\n')
    f.write('%s;%d;%d;%.4g;%.4g;%.4g;%.4g\n' % (values[0], values[1], values[2],
            values[3], values[4], values[5], values[6]))
    f.close()
    print("\nTop polls:")
    headers = ['URL', 'Votes']
    table_values = []
    f = open(OUTPUT_DIR + "polls.csv","w", encoding="utf-8")
    f.write(";".join(headers) + '\n')
    for i, _ in enumerate(polls):
        values = [polls[i][4], polls[i][6]]
        f.write('%s;%d\n' % (values[0], int(values[1])))
        if i <= count:
            table_values.append(values)
    f.close()
    print(tabulate.tabulate(table_values, headers=headers, floatfmt=".4g", numalign="right"))
