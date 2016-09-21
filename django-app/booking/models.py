from __future__ import unicode_literals
from datetime import time

from django.db import models
from django.core.validators import MinValueValidator


class TimeInterval(models.Model):

    default_time = time()
    start_time = models.TimeField(default=default_time)
    finish_time = models.TimeField(default=default_time)

    def __str__(self):
        return "{0} - {1}".format(self.start_time.strftime("%H:%M"), self.finish_time.strftime("%H:%M"))


class Day(models.Model):

    date = models.DateField()

    def __str__(self):
        return "{0}".format(self.date.strftime("%d/%m/%y"))


class RentPeriod(models.Model):

    start_date = models.DateField(db_index=True)
    finish_date = models.DateField(db_index=True)

    def __str__(self):
        return "{0} - {1}".format(self.start_date.strftime("%d/%m/%y"), self.finish_date.strftime("%d/%m/%y"))


class Suite(models.Model):

    name = models.CharField(max_length=128)
    price_per_night = models.IntegerField(default=10, db_index=True)
    rent_periods = models.ManyToManyField(RentPeriod, blank=True, db_index=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class PurchaseInDay(models.Model):
    """ purchased date """
    day = models.ForeignKey(Day)
    time_interval = models.ForeignKey(TimeInterval, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)

    PERSON = r'P'
    GROUP = r'G'
    ACTIVITY_TYPES = (
        (PERSON, 'per person'),
        (GROUP, 'group')
    )
    price_options = models.CharField(
        choices=ACTIVITY_TYPES,
        default=PERSON,
        max_length=1
    )

    def __str__(self):
        return "{0} in {1}".format(self.price_options, self.day.date.strftime("%d/%m/%y"))


class Addon(models.Model):

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price_per_unit = models.IntegerField(default=20)

    availability_days = models.ManyToManyField(Day)
    availability_time_slots = models.ManyToManyField(TimeInterval, blank=True)

    MORNING = r'M'
    EVENING = r'E'
    WHOLE = r'W'
    TIME = r'T'

    TIME_CHOICES = (
        (MORNING, 'Morning'),
        (EVENING, 'Evening'),
        (WHOLE, 'Whole day'),
        (TIME, 'Time slot'),
    )
    unit = models.CharField(
        choices=TIME_CHOICES,
        default=WHOLE,
        max_length=1
    )

    def __str__(self):
        return self.name


class AddonsEntity(models.Model):
    addon = models.ForeignKey(Addon)
    purchased_in_dates = models.ManyToManyField(PurchaseInDay)

    def __str__(self):
        purchases = self.purchased_in_dates.all()
        string_of_purchases = ", ".join((str(pur) for pur in purchases))

        return "{0} on [{1}]".format(self.addon, string_of_purchases)


class Enhance(models.Model):
    addons = models.ManyToManyField(AddonsEntity)

    def __str__(self):
        addons_stack = self.addons.all()
        count = len(addons_stack)
        data = ", ".join((str(stack) for stack in addons_stack))

        return "{0}: {1}".format(count, data)


class Client(models.Model):
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

    SEX_CHOICES = (
        (True, 'Male'),
        (False, 'Female')
    )
    sex = models.BooleanField(choices=SEX_CHOICES, default=True)

    phone = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{0} - {1}".format(self.username, self.email)


class Booking(models.Model):

    created_date = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    period = models.OneToOneField(RentPeriod, on_delete=models.CASCADE)

    suites = models.ManyToManyField(Suite)
    adults = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)

    addons = models.ForeignKey(Enhance, blank=True, null=True, on_delete=models.SET(None))

    total_price = models.PositiveSmallIntegerField(validators=[MinValueValidator(10)])

    def __str__(self):
        suites_stack = self.suites.all()
        data = ", ".join((str(suite) for suite in suites_stack))
        return "{0} created at {1}".format(data, self.created_date.strftime("%H:%M %A %d/%m/%y"))