var gulp = require("gulp");
var util = require('gulp-util');

var less = require('gulp-less');
var cssmin = require('gulp-cssmin');

var rename = require("gulp-rename");
var clean = require('gulp-clean');

var sourcemaps = require("gulp-sourcemaps");
var concat = require("gulp-concat");

var rollup = require("gulp-rollup");
var rollupBabel = require("rollup-plugin-babel");
var babel = require("gulp-babel");

var config = {
    bundleName: "TravelApplication",
    srcLocation: "browser/src",
    distLocation: "django-app/booking/static/dist",
    production: !!util.env.production
};

gulp.task("default", ["less", "javascript"]);

gulp.task('javascript', function() {
  gulp.src(config.srcLocation +'/javascript-es6/*.js')

        .pipe(sourcemaps.init())
        .pipe(rollup({
            // any option supported by Rollup can be set here.
            entry: config.srcLocation +'/javascript-es6/main.js',
            format: 'iife',
            moduleName: config.bundleName,
            plugins: [ rollupBabel() ]
        }))
        .pipe(babel({
            presets: ['es2015-rollup'] // ['react', 'es2015']
        }))
        .pipe(concat("all.js"))
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest(config.distLocation +'/js'));
});

gulp.task('less', function() {
    // less styles from src/less folder
    // only one root file need compile
    gulp.src(config.srcLocation +'/less/main.less')
        .pipe(less())
        .pipe(config.production ? cssmin() : util.noop())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(config.distLocation +'/css'));
});

gulp.task('clean', function() {

    gulp.src(
        [
            config.distLocation +"/css/main.min.css",
            config.distLocation +"/js/all.js",
            config.distLocation +"/js/all.js.map"
        ],
        {read: false}
    )
    .pipe(clean());

});