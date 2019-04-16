
import datetime
import calendar

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from common_data import OUTPUT_DIR

def get_dateposts(name, data, data_range, xticks=None, autolocator=False):
    x = data_range
    y = [data.count(str(i)) for i in x]
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

def dateposts(db):
    #TODO: add csv and print tables
    #TODO: add total info?
    #TODO: add info about likes, reposts and comments and maybe wordcount
    posts = db.get_posts_by_dates()
    times = sorted([datetime.datetime.fromtimestamp(x[0]).strftime('%H') for x in posts]) #hours
    years = sorted([datetime.datetime.fromtimestamp(x[0]).strftime('%Y') for x in posts]) #years
    weekdays = sorted([datetime.datetime.fromtimestamp(x[0]).strftime('%a') for x in posts]) #weekdays
    months = sorted([datetime.datetime.fromtimestamp(x[0]).strftime('%B') for x in posts]) #months
    dates = sorted([datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m') for x in posts]) #dates
    # print(dates)

    years_list = sorted(list(set(years)))
    get_dateposts('posts_years.png', years, years_list)

    sorter = [calendar.month_name[i + 1] for i in range(12)]
    sorterIndex = dict(zip(sorter, range(len(sorter))))
    month_names = sorted(list(set(months)), key=lambda m: sorterIndex[m])
    get_dateposts('posts_months.png', months, month_names)

    sorter = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sorterIndex = dict(zip(sorter, range(len(sorter))))
    weekdays_names = sorted(list(set(weekdays)), key=lambda day: sorterIndex[day])
    get_dateposts('posts_weekdays.png', weekdays, weekdays_names)

    d1 = datetime.datetime.strptime(dates[0], "%Y-%m").date()
    d2 = datetime.datetime.strptime(dates[len(dates) - 1], "%Y-%m").date()
    delta = d2 - d1
    alldates = [(d1 + datetime.timedelta(i)).strftime('%Y-%m') for i in range(delta.days + 1)]
    get_dateposts('posts_allmonths.png', dates, alldates, autolocator=True)

    times_range = [i for i in range(24)]
    get_dateposts('posts_hours.png', times, times_range, ["%02d:00" % (i) for i in times_range])
