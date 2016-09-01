"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */

import booking_controller from './controller';
import checking_controller from "./checking";
import bookingController from './controllers/index';



const $applicationMeta = document.querySelectorAll("meta[name=application-name]");

 if (typeof $applicationMeta[0] !== 'undefined') {

     const moduleName = $applicationMeta[0].content;
     console.log(`Loaded ${ moduleName } module`);

     switch (moduleName) {

         case "booking":
             booking_controller();
             break;
         case "checking":
             checking_controller();
             break;
         case "index":
             bookingController();
             break;
     }


 }
 else {
     console.log("Bad application module");
 }