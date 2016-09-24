from django.contrib import admin

from .models import Client, Booking, Suite, RentPeriod, TimeInterval, \
    Addon, AddonsPurchasing, Enhance, Day, PurchaseInDay

admin.site.register(Client)
admin.site.register(Booking)
admin.site.register(Suite)

admin.site.register(Day)
admin.site.register(TimeInterval)
admin.site.register(RentPeriod)

admin.site.register(Addon)
admin.site.register(AddonsPurchasing)
admin.site.register(Enhance)
admin.site.register(PurchaseInDay)