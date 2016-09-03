#! python
# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from collections import namedtuple


class DateHelper():

    DATE_FORMAT_DEFAULT = "%Y-%m-%d"
    DATE_FORMAT_USA = "%m-%d-%Y"
    DATE_FORMAT_USA_FULL = "%a %b %d %Y"
    TODAY_FORMAT = "%H:%M %d/%m/%y"

    def get_succesful_dates_delta(self, start, end, delta_days=2):
        delta = end - start

        return delta if delta > timedelta(days=delta_days) and start > datetime.today().date() else 0

    def get_overlap_for_range(self, start_interval1, end_interval1, start_interval2, end_interval2):
        Range = namedtuple('Range', ['start', 'end'])

        suite_range = Range(start=start_interval1, end=end_interval1)
        today_interval = Range(start=start_interval2, end=end_interval2)

        latest_start = max(suite_range.start, today_interval.start)
        earliest_end = min(suite_range.end, today_interval.end)

        overlap = (earliest_end - latest_start).days + 1

        return None if overlap < 1 else overlap

    def get_overlap_with_today(self, start, end, days):
        today = date.today()
        end_data = today + timedelta(days=days)

        return self.get_overlap_for_range(start, end, today, end_data)

    def get_string_date_formated(self, check_in_date, check_out_date):

        date_formated = {
            'ymd': {
                'check_in': check_in_date.strftime(self.DATE_FORMAT_DEFAULT),
                'check_out': check_out_date.strftime(self.DATE_FORMAT_DEFAULT)
            },
            'usa': {
                'check_in': check_in_date.strftime(self.DATE_FORMAT_USA),
                'check_out': check_out_date.strftime(self.DATE_FORMAT_USA)
            },
            'usa_full': {
                'check_in': check_in_date.strftime(self.DATE_FORMAT_USA_FULL),
                'check_out': check_out_date.strftime(self.DATE_FORMAT_USA_FULL)
            }
        }

        return date_formated

    def get_date_from_format(self, check_in_str, check_out_str):
        check_in_date = datetime.strptime(check_in_str, self.DATE_FORMAT_DEFAULT).date()
        check_out_date = datetime.strptime(check_out_str, self.DATE_FORMAT_DEFAULT).date()

        return check_in_date, check_out_date

    def get_today_as_string(self):
        return datetime.today().strftime(self.TODAY_FORMAT)