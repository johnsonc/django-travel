from django.contrib import admin

from .models import Client, Booking, Suite, RentPeriod, DateInterval, TimeInterval, Addon, AddonsEntity, AddonsStack

admin.site.register(Client)
admin.site.register(Booking)
admin.site.register(Suite)
admin.site.register(RentPeriod)
admin.site.register(DateInterval)
admin.site.register(TimeInterval)
admin.site.register(Addon)
admin.site.register(AddonsEntity)
admin.site.register(AddonsStack)