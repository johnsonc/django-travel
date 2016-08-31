import logging
from datetime import datetime

from django.shortcuts import render
from django.utils.html import escape
from django.views.decorators.http import require_POST

from .forms import BookingForm
from .models import SuiteEntity, RentPeriod
from time_utility import get_overlap_for_range

logger = logging.getLogger(__name__)


# Index view.
def index(request):

    rent_periods = RentPeriod.objects.all()
    busy_date_range_pks = []

    for period in rent_periods:
        suite_start_date = period.start_date
        suite_end_date = period.finish_date

        overlap = get_overlap_for_range(suite_start_date, suite_end_date, days=4)
        if overlap:
            logger.debug("{0} days overlap in {1} period".format(overlap, period))

            busy_date_range_pks.append(period.pk)

    logger.debug("busy_date_range_pks is {0}".format(busy_date_range_pks))

    free_suites = SuiteEntity.objects.exclude(
                        rent_periods__pk__in=busy_date_range_pks
                        ).order_by('-price_per_night').reverse()

    form = BookingForm()
    today = datetime.today().strftime("%H:%M %d/%m/%y")
    context = {'form': form, 'available_suites': free_suites, 'today': today}

    return render(request, 'booking.html', context)


@require_POST
def check(request):
    logger.debug("require_POST /check")

    pk = int(request.POST['pk'])
    check_in_date = escape(request.POST['check_in_date'])
    check_out_date = escape(request.POST['check_out_date'])

    if pk and check_in_date and check_out_date:
        logger.debug("check_in_date is {0}".format(check_in_date))
        logger.debug("check_out_date is {0}".format(check_out_date))

    suite = SuiteEntity.objects.get(pk=pk)

    today = datetime.today().strftime("%H:%M %d/%m/%y")
    context = {'today': today, 'suite': suite, 'pk': pk, 'check_in_date': check_in_date, 'check_out_date': check_out_date}

    return render(request, 'check.html', context)