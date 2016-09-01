"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */
let start = moment().add(1, 'days');
let end = moment().add(4, 'days');

let min = moment().add(1, 'days');

function changeDateHandler(start, end) {
    let display_format = 'MMMM D, YYYY';
    let django_format = 'YYYY-MM-DD';

    $('#reportrange span').html(
        `${start.format(display_format)} - ${end.format(display_format)}`
    );

    let form = $('#checking_form');
    let checkin_date_field = $("input[name='check_in_date']", form);
    let checkout_date_field = $("input[name='check_out_date']", form);

    checkin_date_field.val(start.format(django_format));
    checkout_date_field.val(end.format(django_format))
}

export default function () {
    $(() => {

        $('#reportrange').daterangepicker({
            startDate: start,
            endDate: end,
            minDate: min,
            ranges: {
               'Next 4 days': [moment().add(1, 'days'), moment().add(4, 'days')],
               'Next week': [moment().add(1, 'days'), moment().add(7, 'days')],
               'Week after': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, changeDateHandler);

        changeDateHandler(start, end);

    });
}