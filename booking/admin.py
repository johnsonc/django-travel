from django.contrib import admin

from .models import Booking, SuiteEntity, RentPeriod

admin.site.register(Booking)
admin.site.register(SuiteEntity)
admin.site.register(RentPeriod)