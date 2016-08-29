from __future__ import unicode_literals

from django.db import models


class SuiteEntity(models.Model):
    name = models.CharField(max_length=128)
    price_per_night = models.IntegerField(default=10)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class BusyDateRangeOfSuite(models.Model):
    start_date = models.DateField()
    finish_date = models.DateField()

    suite = models.ForeignKey(SuiteEntity)

    def __str__(self):
        return "{0} - {1}".format(self.start_date.strftime("%d/%m/%y"), self.finish_date.strftime("%d/%m/%y"))


class Booking(models.Model):
    created_date = models.DateTimeField(auto_now=True)

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    suite = models.ManyToManyField(SuiteEntity)

    def __str__(self):
        return self.created_date.strftime("%A %d/%m/%y")