'use strict';

// requirements

var gulp = require('gulp'),
    browserify = require('gulp-browserify'),
    size = require('gulp-size'),
    clean = require('gulp-clean');


// tasks

gulp.task('clean', function () {
    return gulp.src(['./lolbox/static/bower_components'], {read: false})
        .pipe(clean());
});

gulp.task('default', function () {
    gulp.start('clean');
});
