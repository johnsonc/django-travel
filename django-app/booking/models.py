from __future__ import unicode_literals
from datetime import time

from django.db import models
from django.core.validators import MinValueValidator


class DateInterval(models.Model):

    start_date = models.DateField()
    finish_date = models.DateField()

    def __str__(self):
        return "{0} - {1}".format(self.start_date.strftime("%d/%m/%y"), self.finish_date.strftime("%d/%m/%y"))


class RentPeriod(models.Model):
    interval = models.OneToOneField(DateInterval, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.interval)


class Suite(models.Model):

    name = models.CharField(max_length=128)
    price_per_night = models.IntegerField(default=10)
    rent_periods = models.ManyToManyField(RentPeriod, blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class TimeInterval(models.Model):

    default_time = time()
    start_time = models.TimeField(default=default_time)
    finish_time = models.TimeField(default=default_time)

    def __str__(self):
        return "{0} - {1}".format(self.start_time.strftime("%H:%M"), self.finish_time.strftime("%H:%M"))


class Addon(models.Model):

    name = models.CharField(max_length=128)
    price = models.IntegerField(default=10)

    HALF = 30
    ONE = 60
    TWO = 120
    MINUTES_CHOICES = (
        (HALF, '30 min'),
        (ONE, '1 hour'),
        (TWO, '2 hours'),
    )
    unit = models.PositiveIntegerField(
        choices=MINUTES_CHOICES,
        default=ONE,
    )

    def __str__(self):
        return self.name


class AddonsEntity(models.Model):

    interval = models.ForeignKey(TimeInterval)
    addon = models.ForeignKey(Addon)

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return "{0} in {1}".format(self.addon, self.interval)


class AddonsStack(models.Model):
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
    adults = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    addons = models.ForeignKey(AddonsStack, blank=True, null=True, on_delete=models.SET(None))

    amount = models.PositiveIntegerField(validators=[MinValueValidator(10)])

    def __str__(self):
        suites_stack = self.suites.all()
        data = ", ".join((str(suite) for suite in suites_stack))
        return "{0} created at {1}".format(data, self.created_date.strftime("%H:%M %A %d/%m/%y"))