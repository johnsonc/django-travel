from django.shortcuts import render
from .forms import BookingForm


# Index view.
def index(request):

    form = BookingForm()
    context = {'form': form}

    return render(request, 'booking.html', context)
