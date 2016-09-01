"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */

export default function () {
    $(function () {
        const adultsField = $(".adults");
        const priceField = $(".price_per_one");

        const priceText = priceField.text();
        const pricePerOne = parseInt(priceText.substr(1, priceText.length), 10);

        adultsField.on("change", function () {
            let adults = $(this).val();

            priceField.text(`$${ adults * pricePerOne}`)
        })

    });
}