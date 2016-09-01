import logging
from datetime import datetime

from django.shortcuts import render
from django.utils.html import escape
from django.views.decorators.http import require_POST

from django.http import HttpResponseBadRequest
# from django.template import Context, loader

from .forms import BookingForm
from .models import SuiteEntity, RentPeriod
from time_utility import get_overlap_for_range, get_succesful_dates_delta

logger = logging.getLogger(__name__)


# Index view.
def index(request):

    rent_periods = RentPeriod.objects.all()
    busy_date_range_pks = set()

    for period in rent_periods:
        suite_start_date = period.start_date
        suite_end_date = period.finish_date

        overlap = get_overlap_for_range(suite_start_date, suite_end_date, days=4)
        if overlap:
            logger.debug("{0} days overlap in {1} period".format(overlap, period))

            busy_date_range_pks.add(period.pk)

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

    try:
        pk = int(request.POST['pk'])
        check_in_date = escape(request.POST['check_in_date'])
        check_out_date = escape(request.POST['check_out_date'])

        logger.debug("check_in_date is {0}".format(check_in_date))
        logger.debug("check_out_date is {0}".format(check_out_date))

        check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")

    except Exception as e:
        print(e.message)

        pk = 1
        check_in_date = datetime.today()
        check_out_date = datetime.today()

    if pk and check_in_date and check_out_date:

        check_in_date_formated = check_in_date.strftime("%Y-%m-%d")
        check_out_date_formated = check_out_date.strftime("%Y-%m-%d")

        interval_delta = get_succesful_dates_delta(check_in_date, check_out_date)

        logger.debug("get_datetime_delta is {0}".format(interval_delta))

        if interval_delta:
            logger.debug("OK")

            request.session['check_in_date'] = check_in_date_formated
            request.session['check_out_date'] = check_out_date_formated
            request.session['suit_pk'] = pk

            suite = SuiteEntity.objects.get(pk=pk)

            today = datetime.today().strftime("%H:%M %d/%m/%y")

            interval_date_template = "{0} - {1}"
            interval_date_format = "%a %b %d %Y"

            context = {
                'today': today,
                'suite': suite,
                'pk': pk,
                'check_in_date_format': check_in_date_formated,
                'check_out_date_format': check_out_date_formated,
                'interval_date_format': interval_date_template.format(
                    check_in_date.strftime(interval_date_format),
                    check_out_date.strftime(interval_date_format),
                ),
                'interval_days': interval_delta.days,
                'price_per_one': interval_delta.days * suite.price_per_night
            }

            return render(request, 'check.html', context)

        else:
            context = {
                'request_path': request.path,
                'exception': "Dates range is invalid!!"
            }

            logger.debug(context['exception'])
            request.session.flush()

            # template = loader.get_template('400.html')
            # body = template.render(context, request)
            return HttpResponseBadRequest(context['exception'])
    else:
        return HttpResponseBadRequest("Error POST data")