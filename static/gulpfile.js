/**
 * Gulp Build Configuration
 */

/* jshint browser:false, node:true */

'use strict';

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var rename = require('gulp-rename');
var header = require('gulp-header');
var clean = require('gulp-clean');
var jade = require('gulp-jade');

var pkg = require('./package.json');


var banner =
    '/** \n' +
    ' * <%= pkg.name %> - <%= pkg.description %>\n' +
    ' * @version v<%= pkg.version %>\n' +
    ' * @link <%= pkg.homepage %>\n' +
    ' * @license <%= pkg.license %>\n' +
    ' */\n\n';

var dirs = {
    root: __dirname,
    build: __dirname + '/public/build',
    views: __dirname + '/public/views',
    src: __dirname + '/src'
};

function createCleanTask(task, dirs) {
    gulp.task(task, function() {
        return gulp.src(dirs);
            // .pipe(clean({
            //     force: true,
            //     read: false
            // }));
    });
}

createCleanTask('clean:js', [dirs.build + '/js/**/*']);
createCleanTask('clean:sass', [dirs.build + '/css/**/*']);
createCleanTask('clean:jade', [dirs.views + '/**/*']);

gulp.task('build:sass', ['clean:sass'], function() {
    return gulp.src(dirs.src + '/sass/**/*.scss')
        .pipe(sourcemaps.init())
        .pipe(sass.sync({
            outputStyle: 'compact',
        }).on('error', sass.logError))
        .pipe(autoprefixer({
            cascade: false
        }))
        .pipe(header(banner, {pkg : pkg}))
        .pipe(sourcemaps.write('./',{
            addComment: true,
            includeContent: true
        }))
        .pipe(gulp.dest(dirs.build + '/css'));
});


gulp.task('build:js', ['clean:js'], function() {
    return gulp.src([
            dirs.src + '/js/**/*.js'
        ])
        .pipe(sourcemaps.init())
        .pipe(header(banner, {pkg : pkg}))
        .pipe(rename(function(path){
            path.extname = '.min.js';
        }))
        .pipe(uglify({
            mangle: true,
            compress: true
        }))
        .pipe(sourcemaps.write('./', {
            addComment: true,
            includeContent: true
        }))
        .pipe(gulp.dest(dirs.build + '/js'));
});

gulp.task('build:jade', ['clean:jade'], function() {
    return gulp.src(dirs.src + '/jade/**/[^_]*.jade')
        .pipe(jade({
            pretty: true,
            locals: {}
        }))
        .pipe(gulp.dest(dirs.views));
});

gulp.task('default', ['build:sass', 'build:js', 'build:jade']);

gulp.task('watch', ['default'], function() {
    gulp.watch(dirs.src + '/js/**/*', ['build:js']);
    gulp.watch(dirs.src + '/sass/**/*', ['build:sass']);
    gulp.watch(dirs.src + '/jade/**/*', ['build:jade']);
});
