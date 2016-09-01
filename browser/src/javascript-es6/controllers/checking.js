"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */

export default function () {
    $(function () {
        let adults = 1;

        const adultsField = $(".adults");
        const priceField = $(".price_per_one");

        const priceText = priceField.text();
        const pricePerOne = parseInt(priceText.substr(1, priceText.length), 10);

        const continueButton = $(".continue-block button");
        const checkingForm = $("#checking_form");

        adultsField.on("change", function() {
            adults = $(this).val();

            priceField.text(`$${ adults * pricePerOne}`)
        });

        continueButton.on("click", () => {

            $("input[name=adults]", checkingForm).val(adults);
            checkingForm.submit()
        })

    });
}