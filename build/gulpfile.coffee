gulp = require 'gulp'
browserify = require 'gulp-browserify'
size = require 'gulp-size'
bower = require 'gulp-bower'
gutil = require 'gulp-util'
clean = require 'gulp-clean'
rename = require 'gulp-rename'

gulp.task 'coffee', ->
  gulp.src './lolbox/coffee/main_ui.coffee', {read: false}
  .pipe browserify {transform: ['cjsxify'],
  extensions: ['.coffee']}
  .pipe rename 'app.js'
  .pipe gulp.dest './lolbox/static/js' # destination dir
  .pipe size()

# clean bower components and js
gulp.task 'clean', ->
  gulp.src ['./lolbox/static/bower_components'], {read: false}
  .pipe clean()
  gulp.src ['./lolbox/static/js'], {read: false}
  .pipe clean()

# autocompile coffeescript to js on changes
gulp.task 'watch', ->
  gulp.watch './lolbox/coffee/**', ['coffee']

# install bower components
gulp.task 'bower', ->
  bower './lolbox/static/bower_components'

# main production task
# install bower components
gulp.task 'production', ->
  gulp.start 'bower'
  gulp.start 'coffee'

# main develop task
# clean -> install bower components -> compile coffeescript to js -> start autoreload task
gulp.task 'default', ['clean'], ->
  gulp.start 'bower'
  gulp.start 'coffee'
  gulp.start 'watch'
