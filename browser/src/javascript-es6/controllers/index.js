"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */
import { checkClickHandler, changeDateHandler } from "../handlers/index";

export default function () {

    let start_day = moment().add(1, 'days');
    let end_day = moment().add(4, 'days');

    let min_day = moment().add(1, 'days');

    $(() => {

        $("button.btn.btn-default.btn-lg").on("click", checkClickHandler);

        $('#reportrange').daterangepicker({
            startDate: start_day,
            endDate: end_day,
            minDate: min_day,
            ranges: {
               'Next 4 days': [moment().add(1, 'days'), moment().add(4, 'days')],
               'Next week': [moment().add(1, 'days'), moment().add(7, 'days')],
               'Month later': [moment().add(1, 'month'), moment().add(1, 'month').add(4, 'days')]
            }
        }, changeDateHandler);

        changeDateHandler(start_day, end_day);

    });
}