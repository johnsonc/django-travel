import logging
from datetime import datetime

from django.shortcuts import render
from django.utils.html import escape
from django.views.decorators.http import require_POST

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader

from .models import Client, Suite, RentPeriod, DateInterval, Addon, Booking
from time_utility import DateHelper

logger = logging.getLogger(__name__)
TEMPLATE_404 = loader.get_template('error_400.html')


# Index view.
def index(request):
    date_help = DateHelper()

    rent_periods = RentPeriod.objects.all()
    busy_date_range_pks = set()

    for period in rent_periods:
        suite_start_date = period.interval.start_date
        suite_end_date = period.interval.finish_date

        overlap = date_help.get_overlap_with_today(suite_start_date, suite_end_date, days=4)
        if overlap:
            logger.debug("{0} days overlap in {1} period".format(overlap, period))

            busy_date_range_pks.add(period.pk)

    logger.debug("busy_date_range_pks is {0}".format(busy_date_range_pks))

    free_suites = Suite.objects.exclude(
        rent_periods__pk__in=busy_date_range_pks
    ).order_by('-price_per_night').reverse()

    today_str = datetime.today().strftime("%H:%M %d/%m/%y")
    context = {'available_suites': free_suites, 'today': today_str}

    return render(request, 'index.html', context)


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
            date_help = DateHelper()

            try:
                check_in_date_object, check_out_date_object = date_help.get_date_from_format(
                    check_in_date,
                    check_out_date
                )

                logger.debug("check_in_date_object is {0}".format(check_in_date_object))
                logger.debug("check_out_date_object is {0}".format(check_out_date_object))

            except Exception as e:
                logger.warning(e.message)

                context = {
                    'exception': "Dates format is invalid!"
                }

                body = TEMPLATE_404.render(context, request)

                return HttpResponseBadRequest(body)

            #  (start, end, delta_days=2)
            rent_interval = date_help.get_succesful_dates_delta(start=check_in_date_object, end=check_out_date_object)

            logger.debug("get_datetime_delta is {0} days".format(rent_interval))

            if rent_interval:
                dates_formated = date_help.get_string_date_formated(check_in_date_object, check_out_date_object)

                request.session['check_in_date'] = dates_formated['ymd']['check_in']
                request.session['check_out_date'] = dates_formated['ymd']['check_out']
                request.session['suite'] = pk

                suite = Suite.objects.get(pk=pk)

                rent_periods = suite.rent_periods.all()

                logger.debug("{0} rent_periods for Suite instance".format(len(rent_periods)))

                suite_rented_for_check_interval = False

                for period in rent_periods:
                    suite_start_date = period.interval.start_date
                    suite_end_date = period.interval.finish_date

                    overlap = date_help.get_overlap_for_range(
                        suite_start_date,
                        suite_end_date,

                        check_in_date_object,
                        check_out_date_object)

                    logger.debug(
                        "overlap now is {0} for period {1} vs (check_in_date={2},check_out_date={3})"
                        .format(overlap, period, dates_formated['usa']['check_in'], dates_formated['usa']['check_out']))

                    if overlap:
                        suite_rented_for_check_interval = True
                        break

                interval_date_template = "{0} - {1}"

                addons = Addon.objects.all()

                context = {
                    'today': date_help.get_today_as_string(),
                    'suite': suite,
                    'busy': suite_rented_for_check_interval,
                    'pk': pk,
                    'check_in_date_format': dates_formated['usa']['check_in'],
                    'check_out_date_format': dates_formated['usa']['check_out'],
                    'interval_date_format': interval_date_template.format(
                        dates_formated['usa_full']['check_in'], dates_formated['usa_full']['check_out']
                    ),
                    'interval_days': rent_interval.days,
                    'price_per_one': rent_interval.days * suite.price_per_night,
                    'addons': addons
                }

                return render(request, 'check.html', context)

            else:
                context = {
                    'exception': "Dates interval is invalid or small, you can rent minimum 2 days!"
                }

                logger.debug(context['exception'])
                request.session.flush()

                body = TEMPLATE_404.render(context, request)
                return HttpResponseBadRequest(body)
        else:
            context = {
                'exception': "Dates range is invalid!"
            }

            logger.debug(context['exception'])
            request.session.flush()

            body = TEMPLATE_404.render(context, request)
            return HttpResponseBadRequest(body)

    except Exception as e:
        logger.warning(e.message)

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

        date_help = DateHelper()

        logger.debug("[request.session] check_in_date is {0}".format(check_in_date))
        logger.debug("[request.session] check_out_date is {0}".format(check_out_date))

        check_in_date, check_out_date = date_help.get_date_from_format(check_in_date, check_out_date)

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

        today = date_help.get_today_as_string()

        dates_formated = date_help.get_string_date_formated(check_in_date, check_out_date)

        check_in_date_formated = dates_formated['usa']['check_in']
        check_out_date_formated = dates_formated['usa']['check_out']

        interval_date_template = "{0} - {1}"

        rent_interval = date_help.get_succesful_dates_delta(start=check_in_date, end=check_out_date)

        logger.debug("get_datetime_delta is {0} days".format(rent_interval.days))

        if rent_interval:

            request.session['adults'] = adults

            context = {
                'today': today,
                'suite': suite,
                'check_in_date_format': check_in_date_formated,
                'check_out_date_format': check_out_date_formated,
                'interval_date_format': interval_date_template.format(
                    dates_formated['usa_full']['check_in'], dates_formated['usa_full']['check_out']
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

        # TODO: remove it!
        username = username or "User"
        email = email or "user@webserver.com"
        # TODO: warning

        suite_pk = int(request.session['suite'])
        adults = int(request.session['adults'])

        date_help = DateHelper()

        check_in_date, check_out_date = date_help.get_date_from_format(
            request.session['check_in_date'],
            request.session['check_out_date']
        )

        rent_interval = date_help.get_succesful_dates_delta(start=check_in_date, end=check_out_date)

        suite = Suite.objects.get(pk=suite_pk)

        price = rent_interval.days * suite.price_per_night * adults

        # Saving a new models
        new_date_interval = DateInterval.objects.create(start_date=check_in_date, finish_date=check_out_date)
        new_rent_period = RentPeriod.objects.create(interval=new_date_interval)

        client, created = Client.objects.get_or_create(username=username, email=email)

        try:
            new_booking, created = Booking.objects.update_or_create(
                client=client,
                period=new_rent_period,
                adults=adults,
                amount=price)

            new_booking.suites.add(suite)
            suite.rent_periods.add(new_rent_period)

        except Exception as e:
            logger.warning("Exception = {0}".format(e.message))

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

        body = TEMPLATE_404.render(context, request)
        return HttpResponseBadRequest(body)