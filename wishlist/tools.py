import datetime

def get_date_range(start, finish):
    for i in range(int((finish - start).days) + 1):
        yield start + datetime.timedelta(i)


def find_weeks(start, finish):
    _list = []
    for i in range((finish - start).days + 1):
        day = (start + datetime.timedelta(days=i))
        week_day = day.isocalendar()
        yearweek = f'Year {week_day[0]} - Week {week_day[1]}'

        _list.append({
            'week_day': day,
            'week': yearweek
        })
    return _list
