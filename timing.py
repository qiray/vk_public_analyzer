
import datetime
import calendar

from mpl_toolkits.axes_grid1 import host_subplot
import mpl_toolkits.axisartist as AA
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from common_data import OUTPUT_DIR

def get_dateposts(name, data, data_range, xticks=None, autolocator=False):
    #https://matplotlib.org/examples/axes_grid/demo_parasite_axes2.html
    x = data_range
    y1 = [posts_count(data, str(i)) for i in x] #posts
    y2 = [get_count(data, str(i), 1) for i in x] #likes
    y3 = [get_count(data, str(i), 2) for i in x] #reposts
    # y4 = [get_count(data, str(i), 3) for i in x] #comments
    # y5 = [get_count(data, str(i), 4) for i in x] #views
    # y6 = [get_count(data, str(i), 5) for i in x] #attachments
    # y7 = [get_count(data, str(i), 6) for i in x] #text length

    host = host_subplot(111, axes_class=AA.Axes)
    plt.subplots_adjust(right=0.75, bottom=0.15)

    par1 = host.twinx()
    par2 = host.twinx()

    new_fixed_axis = par2.get_grid_helper().new_fixed_axis
    par1.axis["right"] = new_fixed_axis(loc="right", axes=par1)
    par2.axis["right"] = new_fixed_axis(loc="right", axes=par2, offset=(60, 0))

    par2.axis["right"].toggle(all=True)
    host.set_ylabel("posts")
    par1.set_ylabel("likes")
    par2.set_ylabel("reposts")

    if xticks:
        plt.xticks(x, xticks, rotation=45)
    else:
        plt.xticks(rotation=45)
    if autolocator:
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
        plt.gca().xaxis.set_minor_locator(ticker.AutoMinorLocator())

    p1, = host.plot(x, y1, marker='o', label='posts')
    p2, = par1.plot([i for i in range(len(x))], y2, marker='o', label='likes')
    p3, = par2.plot([i for i in range(len(x))], y3, marker='o', label='reposts')

    host.axis["left"].label.set_color(p1.get_color())
    par1.axis["right"].label.set_color(p2.get_color())
    par2.axis["right"].label.set_color(p3.get_color())

    host.legend()

    # plt.plot(x, y1, marker='o', label='posts')
    # plt.plot(x, y2, marker='o', label='likes')
    # plt.plot(x, y3, marker='o', label='reposts')
    # plt.plot(x, y4, marker='o', label='comments')
    # plt.plot(x, y5, marker='o', label='views')
    # plt.plot(x, y6, marker='o', label='attachments')
    # plt.plot(x, y7, marker='o', label='text length')

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
    
    posts = db.get_posts_by_dates()
    #TODO: add total info?
    
    years = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%Y'))
    months = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%B'))
    weekdays = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%a'))
    dates = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m'))
    hours = datalist_to_dict(posts, lambda x: datetime.datetime.fromtimestamp(x[0]).strftime('%H'))

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

    hours_range = [i for i in range(24)]
    get_dateposts('hours.png', hours, hours_range, ["%02d:00" % (i) for i in hours_range])
