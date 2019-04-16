
import datetime
import calendar

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from common_data import OUTPUT_DIR

def get_dateposts(name, y_func, data, data_range, xticks=None, autolocator=False):
    x = data_range
    y = [y_func(data, str(i)) for i in x]
    if xticks:
        plt.xticks(x, xticks, rotation=45)
    else:
        plt.xticks(rotation=45)
    if autolocator:
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
        plt.gca().xaxis.set_minor_locator(ticker.AutoMinorLocator())
    plt.subplots_adjust(bottom=0.15)
    plt.plot(x, y, marker='o')
    plt.savefig(OUTPUT_DIR + name)
    plt.close()

def posts_count(data, value):
    if value in data:
        return len(data[value])
    return 0

def likes_count(data, value):
    if value in data:
        return sum([x[1] for x in data[value]])
    return 0

def drawplots(db):
    posts = db.get_posts_by_dates()
    draw(posts, posts_count, 'posts')
    draw(posts, likes_count, 'likes')

def datalist_to_dict(data, converter):
    result = {}
    for value in data:
        index = converter(value)
        if not index in result:
            result[index] = [value]
        else:
            result[index].append(value)
    return result

def draw(posts, func, name):
    #TODO: add total info?
    #TODO: all data on one plot
    #TODO: add info about likes, reposts and comments and maybe wordcount
    
    years = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%Y'))
    months = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%B'))
    weekdays = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%a'))
    dates = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m'))
    hours = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%H'))

    years_list = sorted(years.keys())
    get_dateposts(name + '_years.png', func, years, years_list)

    sorter = [calendar.month_name[i + 1] for i in range(12)]
    sorterIndex = dict(zip(sorter, range(len(sorter))))
    month_names = sorted(months.keys(), key=lambda m: sorterIndex[m])
    get_dateposts(name + '_months.png', func, months, month_names)

    sorter = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sorterIndex = dict(zip(sorter, range(len(sorter))))
    weekdays_names = sorted(weekdays.keys(), key=lambda day: sorterIndex[day])
    get_dateposts(name + '_weekdays.png', func, weekdays, weekdays_names)

    d1 = datetime.datetime.strptime(min(dates), "%Y-%m").date()
    d2 = datetime.datetime.strptime(max(dates), "%Y-%m").date()
    delta = d2 - d1
    alldates = [(d1 + datetime.timedelta(i)).strftime('%Y-%m') for i in range(delta.days + 1)]
    get_dateposts(name + '_allmonths.png', func, dates, alldates, autolocator=True)

    hours_range = [i for i in range(24)]
    get_dateposts(name + '_hours.png', func, hours, hours_range, ["%02d:00" % (i) for i in hours_range])
