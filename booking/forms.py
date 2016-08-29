#! python
# -*- coding: utf-8 -*-
from django import forms
from .models import Booking
from django.contrib.admin import widgets


class BookingForm(forms.ModelForm):
    created_date = forms.DateField(widget=widgets.AdminDateWidget)

    class Meta:
        model = Booking

        fields = ('created_date', )
