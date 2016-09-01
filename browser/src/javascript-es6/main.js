"use strict";
/**
 * developer: menangen@gmail.com
 * Date: 31.08.16
 * Time: 9:05
 */

import bookingController from './controllers/index';
import checkingController from "./controllers/checking";

const $applicationMeta = document.querySelectorAll("meta[name=application-name]");

 if (typeof $applicationMeta[0] !== 'undefined') {

     const moduleName = $applicationMeta[0].content;
     console.log(`Loaded ${ moduleName } module`);

     switch (moduleName) {

        case "index":
             bookingController();
             break;
         case "checking":
             checkingController();
             break;
     }

 }
 else {
     console.log("Bad application module");
 }