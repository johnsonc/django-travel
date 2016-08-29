#! python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets

from .models import Booking


class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=widgets.AdminDateWidget)
    check_out_date = forms.DateField(widget=widgets.AdminDateWidget)

    class Meta:
        model = Booking

        fields = ('check_in_date', 'check_out_date')
