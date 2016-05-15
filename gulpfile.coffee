gulp = require 'gulp'
gutil = require 'gulp-util'
clean = require 'gulp-clean'
#cjsx = require 'gulp-cjsx'
bower = require 'gulp-bower'

# clean bower packages
gulp.task 'clean', ->
  gulp.src ['./lolbox/static/bower_components'], {read: false}
  .pipe clean()

#gulp.task 'cjsx', ->
#  gulp.src './src/*.cjsx'
#  .pipe cjsx({bare: true})
#  .on 'error', gutil.log
#  .pipe gulp.dest './public/'

gulp.task 'bower', ->
  gutil.log 'Installing bower packages...'
  bower

gulp.task 'production', ->
  gulp.start 'bower'

gulp.task 'dev', ->
  gulp.start 'clean'
  gulp.start 'bower'
# gulp.start 'cjsx'
