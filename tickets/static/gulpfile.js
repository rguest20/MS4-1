var gulp = require('gulp');
var gulpless = require('gulp-less');
var gulpautoprefixer = require('gulp-autoprefixer');
var gulpplumber = require('gulp-plumber');
var babel = require('gulp-babel')
//Creating a Style task that convert LESS to CSS
gulp.task('styles',function(){
    var srcfile = './less/style.less';
    var output = './css';
         return gulp
                 .src(srcfile)
                 .pipe(gulpplumber())
                 .pipe(gulpless())
                 .pipe(gulpautoprefixer())
                 .pipe(gulp.dest(output));
  });

gulp.task('javascript', function(){
  var src = './js/custom.js';
  var out = './js/dist/';
    return gulp
              .src(src)
              .pipe(gulpplumber())
              .pipe(babel())
              .pipe(gulp.dest(out))
})

gulp.task('watch', function(){
  gulp.watch('less/*.less', ['styles']);
  gulp.watch('less/components/*.less', ['styles']);
  gulp.watch('js/*.js', ['javascript'])
})
