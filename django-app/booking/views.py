import logging
from datetime import datetime

from django.shortcuts import render
from django.utils.html import escape
from django.views.decorators.http import require_POST

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

from .forms import BookingForm
from .models import Suite, RentPeriod, DateInterval, Addon, Booking
from time_utility import get_overlap_for_range, get_succesful_dates_delta

logger = logging.getLogger(__name__)
TEMPLATE_404 = loader.get_template('error_400.html')


# Index view.
def index(request):
    rent_periods = RentPeriod.objects.all()
    busy_date_range_pks = set()

    for period in rent_periods:
        suite_start_date = period.interval.start_date
        suite_end_date = period.interval.finish_date

        overlap = get_overlap_for_range(suite_start_date, suite_end_date, days=4)
        if overlap:
            logger.debug("{0} days overlap in {1} period".format(overlap, period))

            busy_date_range_pks.add(period.pk)

    logger.debug("busy_date_range_pks is {0}".format(busy_date_range_pks))

    free_suites = Suite.objects.exclude(
        rent_periods__pk__in=busy_date_range_pks
    ).order_by('-price_per_night').reverse()

    today = datetime.today().strftime("%H:%M %d/%m/%y")
    context = {'available_suites': free_suites, 'today': today}

    return render(request, 'index.html', context)


def booking(request):

    rent_periods = DateInterval.objects.all()
    busy_date_range_pks = set()

    for period in rent_periods:
        suite_start_date = period.start_date
        suite_end_date = period.finish_date

        overlap = get_overlap_for_range(suite_start_date, suite_end_date, days=4)
        if overlap:
            logger.debug("{0} days overlap in {1} period".format(overlap, period))

            busy_date_range_pks.add(period.pk)

    logger.debug("busy_date_range_pks is {0}".format(busy_date_range_pks))

    free_suites = Suite.objects.exclude(
                        rent_periods__pk__in=busy_date_range_pks
                        ).order_by('-price_per_night').reverse()

    form = BookingForm()
    today = datetime.today().strftime("%H:%M %d/%m/%y")
    context = {'form': form, 'available_suites': free_suites, 'today': today}

    return render(request, 'invoice.html', context)


# Form1 sending view: 1 step
@require_POST
def check(request):
    logger.debug("require_POST /check")

    try:
        pk = int(request.POST['pk'])
        check_in_date = request.POST['check_in_date']
        check_out_date = request.POST['check_out_date']

        logger.debug("check_in_date is {0}".format(check_in_date))
        logger.debug("check_out_date is {0}".format(check_out_date))

        if pk and check_in_date and check_out_date:

            try:
                check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")

            except Exception as e:
                logger.warning(e.message)

                context = {
                    'exception': "Dates format is invalid!"
                }

                body = TEMPLATE_404.render(context, request)

                return HttpResponseBadRequest(body)

            check_in_date_formated = check_in_date.strftime("%m-%d-%Y")
            check_out_date_formated = check_out_date.strftime("%m-%d-%Y")

            #  (start, end, delta_days=2)
            rent_interval = get_succesful_dates_delta(start=check_in_date, end=check_out_date)

            logger.debug("get_datetime_delta is {0} days".format(rent_interval.days))

            if rent_interval:

                request.session['check_in_date'] = check_in_date.strftime("%Y-%m-%d")
                request.session['check_out_date'] = check_out_date.strftime("%Y-%m-%d")
                request.session['suite'] = pk

                suite = Suite.objects.get(pk=pk)

                today = datetime.today().strftime("%H:%M %d/%m/%y")

                interval_date_template = "{0} - {1}"
                interval_date_format = "%a %b %d %Y"

                addons = Addon.objects.all()

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
                    'interval_days': rent_interval.days,
                    'price_per_one': rent_interval.days * suite.price_per_night,
                    'addons': addons
                }

                return render(request, 'check.html', context)

        else:
            context = {
                'exception': "Dates range is invalid!"
            }

            logger.debug(context['exception'])
            request.session.flush()

            body = TEMPLATE_404.render(context, request)
            return HttpResponseBadRequest(body)

    except:

        context = {
            'exception': "Error POST data!"
        }

        logger.debug(context['exception'])
        request.session.flush()

        body = TEMPLATE_404.render(context, request)
        return HttpResponseBadRequest(body)


# Form2 sending view: 2 step
@require_POST
def invoice(request):
    try:
        adults = int(request.POST['adults'])
        logger.debug("adults is {0} and type {1}".format(adults, type(adults)))

        suite_pk = int(request.session['suite'])
        logger.debug("suite id is {0}".format(suite_pk))

        check_in_date = request.session['check_in_date']
        check_out_date = request.session['check_out_date']

        logger.debug("[request.session] check_in_date is {0}".format(check_in_date))
        logger.debug("[request.session] check_out_date is {0}".format(check_out_date))

        check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")

    except Exception as e:
        logger.warning("Exception = {0}".format(e.message))
        request.session.flush()

        context = {
            'exception': "POST data is invalid!"
        }

        logger.debug(context['exception'])
        request.session.flush()

        body = TEMPLATE_404.render(context, request)
        return HttpResponseBadRequest(body)

    if adults in xrange(1, 13) and suite_pk:

        suite = Suite.objects.get(pk=suite_pk)

        today = datetime.today().strftime("%H:%M %d/%m/%y")

        check_in_date_formated = check_in_date.strftime("%m-%d-%Y")
        check_out_date_formated = check_out_date.strftime("%m-%d-%Y")

        interval_date_template = "{0} - {1}"
        interval_date_format = "%a %b %d %Y"

        rent_interval = get_succesful_dates_delta(start=check_in_date, end=check_out_date)

        logger.debug("get_datetime_delta is {0} days".format(rent_interval.days))

        if rent_interval:

            request.session['adults'] = adults

            context = {
                'today': today,
                'suite': suite,
                'check_in_date_format': check_in_date_formated,
                'check_out_date_format': check_out_date_formated,
                'interval_date_format': interval_date_template.format(
                    check_in_date.strftime(interval_date_format),
                    check_out_date.strftime(interval_date_format),
                ),
                'interval_days': rent_interval.days,
                'adults': adults,
                'price': rent_interval.days * suite.price_per_night * adults,
                'addons': None
            }

            return render(request, 'invoice.html', context)

    context = {
        'exception': "POST data is invalid!"
    }

    logger.debug(context['exception'])
    request.session.flush()

    body = TEMPLATE_404.render(context, request)
    return HttpResponseBadRequest(body)


# Display Success view: last step
@require_POST
def result(request):
    try:
        username = escape(request.POST['username'])
        email = escape(request.POST['email'])

        suite_pk = int(request.session['suite'])
        adults = int(request.session['adults'])

        check_in_date = datetime.strptime(request.session['check_in_date'], "%Y-%m-%d")
        check_out_date = datetime.strptime(request.session['check_out_date'], "%Y-%m-%d")

        rent_interval = get_succesful_dates_delta(start=check_in_date, end=check_out_date)

        suite = Suite.objects.get(pk=suite_pk)

        price = rent_interval.days * suite.price_per_night * adults

        # Saving a new models
        new_date_interval = DateInterval()
        new_rent_period = RentPeriod(interval=new_date_interval)
        new_booking = Booking(period=new_rent_period)

        # TODO: remove it!
        username = username or "User"
        email = email or "user@webserver.com"
        # TODO: warning

        context = {
            'name': username,
            'email': email,
            'suite': suite.name,
            'days': rent_interval.days
        }

        return render(request, 'result.html', context)

    except Exception as e:
        logger.warning("Exception = {0}".format(e.message))
        request.session.flush()

        context = {
            'exception': "POST data is invalid!"
        }

        logger.debug(context['exception'])
        request.session.flush()

        body = TEMPLATE_404.render(context, request)
        return HttpResponseBadRequest(body)