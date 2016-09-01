#! python
# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from collections import namedtuple


def get_succesful_dates_delta(start, end, delta_days=2):
    delta = end - start

    return delta if delta > timedelta(days=delta_days) and start > datetime.today() else 0


def get_overlap_for_range(start, end, days):
    Range = namedtuple('Range', ['start', 'end'])

    today = date.today()
    end_data = today + timedelta(days=days)

    suite_range = Range(start=start, end=end)
    today_interval = Range(start=today, end=end_data)

    latest_start = max(suite_range.start, today_interval.start)
    earliest_end = min(suite_range.end, today_interval.end)

    overlap = (earliest_end - latest_start).days + 1

    return None if overlap < 1 else overlap