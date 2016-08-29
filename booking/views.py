from django.shortcuts import render
from .forms import BookingForm


# Index view.
def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    form = BookingForm()
    context = {'form': form}

    return render(request, 'booking.html', context)
