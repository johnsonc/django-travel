from django.contrib import admin

from .models import Booking, SuiteEntity, BusyDateRangeOfSuite

admin.site.register(Booking)
admin.site.register(SuiteEntity)
admin.site.register(BusyDateRangeOfSuite)