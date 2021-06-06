var gulp = require('gulp');
var gulpless = require('gulp-less');
var gulpautoprefixer = require('gulp-autoprefixer');
//Creating a Style task that convert LESS to CSS
gulp.task('styles',function(){
    var srcfile = './less/style.less';
    var output = './css';
         return gulp
                 .src(srcfile)
                 .pipe(gulpless())
                 .on('error', swallowError)
                 .pipe(gulpautoprefixer())
                 .pipe(gulp.dest(output));
  });

gulp.task('watch', function(){
  gulp.watch('less/*.less', ['styles']);
  gulp.watch('less/components/*.less', ['styles']);
})

function swallowError (error) {

  // If you want details of the error in the console
  console.log(error.toString())

  this.emit('end')
}
