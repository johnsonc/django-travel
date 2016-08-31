/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 11:42
 */
import checkClickHandler from './handlers.js';

export default function () {
    if (typeof django !== 'undefined') {django.jQuery("button.btn.btn-default.btn-lg").on("click", checkClickHandler)}
}