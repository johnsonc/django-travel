"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */

import booking_controller from './controller';
import checking_controller from "./checking";



const $applicationMeta = document.querySelectorAll("meta[name=application-name]");

 if (typeof $applicationMeta[0] !== 'undefined') {

     const moduleName = $applicationMeta[0].content;
     console.log(`Nice module ${ moduleName }`);

     switch (moduleName) {

         case "booking":
             booking_controller();
             break;
         case "checking":
             checking_controller();
             break;
     }


 }
 else {
     console.log("Bad application module");
 }