/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:43
 */
export function checkClickHandler() {
    $("#checking_form_pk").val(this.name);
    $("#checking_form").submit()
}

export function changeDateHandler(start, end) {
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