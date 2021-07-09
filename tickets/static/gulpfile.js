//Dependencies
const { gulp, watch } = require('gulp');
const { src, dest} = require('gulp');
var gulpless = require('gulp-less');
var gulpautoprefixer = require('gulp-autoprefixer');
var gulpplumber = require('gulp-plumber');
var babel = require('gulp-babel')
var livereload = require('gulp-livereload')

//Creating a Style task that convert LESS to CSS
function styles(done){
  var output = './css';
   return src('./less/style.less')
     .pipe(gulpplumber())
     .pipe(gulpless())
     .pipe(gulpautoprefixer())
     .pipe(dest(output))
     .pipe(livereload())
  done()
}

//Creating a JavaScript task that compiles JS to ES5 (for minification)
function javascript2es5(done) {
  var output = './js/dist/';
    return src('./js/custom.js')
      .pipe(gulpplumber())
      .pipe(babel())
      .pipe(dest(output))
      .pipe(livereload())
  done()
}

//Watch task to update and compile when changes are made.
exports.default = function() {
    livereload.listen()
    watch('less/*.less', styles);
    watch('less/components/*.less', styles);
    watch('js/*.js', javascript2es5)}
