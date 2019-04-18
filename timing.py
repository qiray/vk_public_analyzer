
import calendar
import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot

from common_data import OUTPUT_DIR

def get_element(data, index):
    result = int(index)
    if index < 0:
        return data[0]
    elif index >= len(data):
        return data[-1]
    return data[result]

def draw_subplot(host, fixed_axis, x_range, y, offset, label):
    par = host.twinx()
    par.axis["right"] = fixed_axis(loc="right", axes=par, offset=(offset, 0))
    par.set_ylabel(label)
    p, = par.plot(x_range, y, marker='o', label=label)
    par.axis["right"].label.set_color(p.get_color())

def get_dateposts(name, data, data_range, autolocator=False):
    x = data_range
    y1 = [posts_count(data, str(i)) for i in x] #posts
    y2 = [get_count(data, str(i), 1) for i in x] #likes
    y3 = [get_count(data, str(i), 2) for i in x] #reposts
    y4 = [get_count(data, str(i), 3) for i in x] #comments
    y5 = [get_count(data, str(i), 4) for i in x] #views
    y6 = [get_count(data, str(i), 5) for i in x] #attachments
    y7 = [get_count(data, str(i), 6) for i in x] #text length

    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.65, bottom=0.15, left=0.05)
    new_fixed_axis = host.get_grid_helper().new_fixed_axis

    plt.xticks([])
    x_range = [i for i in range(len(x))]
    host.tick_params(labelrotation=45)
    host.set_xticks(x_range)
    host.set_xticklabels(x)
    if autolocator:
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(
            lambda i, pos: get_element(x, i)))

    host.set_ylabel("posts")
    p1, = host.plot(x_range, y1, marker='o', label='posts')
    host.axis["left"].label.set_color(p1.get_color())

    draw_subplot(host, new_fixed_axis, x_range, y2, 0, 'likes')
    draw_subplot(host, new_fixed_axis, x_range, y3, 60, 'reposts')
    draw_subplot(host, new_fixed_axis, x_range, y4, 120, 'comments')
    draw_subplot(host, new_fixed_axis, x_range, y5, 180, 'views')
    draw_subplot(host, new_fixed_axis, x_range, y6, 240, 'attachments')
    draw_subplot(host, new_fixed_axis, x_range, y7, 300, 'text length')

    host.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
        fancybox=True, shadow=True, ncol=7)
    plt.grid(True)

    fig = plt.gcf()
    fig.set_size_inches(15, 6)
    plt.savefig(OUTPUT_DIR + name)
    plt.close()

def posts_count(data, value):
    if value in data:
        return len(data[value])
    return 0

def get_count(data, value, index):
    if value in data:
        return sum([x[index] for x in data[value]])
    return 0

def datalist_to_dict(data, converter):
    result = {}
    for value in data:
        index = converter(value)
        if not index in result:
            result[index] = [value]
        else:
            result[index].append(value)
    return result

def drawplots(db):
    print('Drawing plots')
    posts = db.get_posts_by_dates()
    #TODO: add total info?
    
    years = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%Y'))
    months = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%B'))
    weekdays = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%a'))
    dates = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m'))
    hours = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%H:00'))

    years_list = sorted(years.keys())
    get_dateposts('years.png', years, years_list)

    sorter = [calendar.month_name[i + 1] for i in range(12)]
    sorterIndex = dict(zip(sorter, range(len(sorter))))
    month_names = sorted(months.keys(), key=lambda m: sorterIndex[m])
    get_dateposts('months.png', months, month_names)

    sorter = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sorterIndex = dict(zip(sorter, range(len(sorter))))
    weekdays_names = sorted(weekdays.keys(), key=lambda day: sorterIndex[day])
    get_dateposts('weekdays.png', weekdays, weekdays_names)

    d1 = datetime.datetime.strptime(min(dates), "%Y-%m").date()
    d2 = datetime.datetime.strptime(max(dates), "%Y-%m").date()
    delta = d2 - d1
    alldates = [(d1 + datetime.timedelta(i)).strftime('%Y-%m') for i in range(delta.days + 1)]
    get_dateposts('allmonths.png', dates, alldates, autolocator=True)

    hours_range = [str.format("%02d:00" % (i)) for i in range(24)]
    get_dateposts('hours.png', hours, hours_range, True)
