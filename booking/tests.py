# from django.test import TestCase
from datetime import date
from time_utility import get_overlap_for_range

suite_start_date = date(2016, 8, 20)
suite_end_date = date(2016, 8, 30)

rent_days = 4

print(get_overlap_for_range(suite_start_date, suite_end_date, days=rent_days))