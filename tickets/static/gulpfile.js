//Dependencies
var gulp = require('gulp');
var gulpless = require('gulp-less');
var gulpautoprefixer = require('gulp-autoprefixer');
var gulpplumber = require('gulp-plumber');
var babel = require('gulp-babel')
var livereload = require('gulp-livereload')

//Creating a Style task that convert LESS to CSS
gulp.task('styles',function(){
  var srcfile = './less/style.less';
  var output = './css';
   return gulp
     .src(srcfile)
     .pipe(gulpplumber())
     .pipe(gulpless())
     .pipe(gulpautoprefixer())
     .pipe(gulp.dest(output))
     .pipe(livereload())
});

//Creating a JavaScript task that compiles JS to ES5 (for minification)
gulp.task('javascript2es5', function(){
  var src = './js/custom.js';
  var out = './js/dist/';
    return gulp
      .src(src)
      .pipe(gulpplumber())
      .pipe(babel())
      .pipe(gulp.dest(out))
      .pipe(livereload())
})

//Watch task to update and compile when changes are made.
gulp.task('watch', function(){
  livereload.listen();
  gulp.watch('less/*.less', ['styles']);
  gulp.watch('less/components/*.less', ['styles']);
  gulp.watch('js/*.js', ['javascript2es5'])
})
