/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:43
 */
function checkClickHandler() {
    django.jQuery("#checking_form_pk").val(this.name);
    django.jQuery("#checking_form").submit()
}

export default checkClickHandler;