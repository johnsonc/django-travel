from django.shortcuts import render
from .forms import BookingForm

from .models import SuiteEntity


# Index view.
def index(request):

    suites = SuiteEntity.objects.order_by('-price_per_night').reverse()[:5]
    form = BookingForm()

    context = {'form': form, 'available_suites': suites}

    return render(request, 'booking.html', context)
