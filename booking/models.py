from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Booking(models.Model):
    created_date = models.DateField()