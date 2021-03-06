// The build will inline common dependencies into this file.
// For any third party dependencies, like jQuery, place them in the lib folder.
// Configure loading modules from the lib directory,
// except for 'app' ones, which are in a sibling
// directory.
requirejs.config({
    baseUrl: '/static/js',
    urlArgs: 'bust=' + (new Date()).getTime(),
    paths: {
        'jquery': '../vendor/jquery/dist/jquery',

        'es6': '../vendor/requirejs-babel/es6',
        'babel': '../vendor/requirejs-babel/babel-5.8.34.min',

        // Foundation
        'foundation': '../vendor/foundation-sites/js/foundation.core',
        'foundation.equalizer': '../vendor/foundation-sites/js/foundation.equalizer',
        'foundation.util.box': '../vendor/foundation-sites/js/foundation.util.box',
        'foundation.util.keyboard': '../vendor/foundation-sites/js/foundation.util.keyboard',
        'foundation.util.mediaQuery': '../vendor/foundation-sites/js/foundation.util.mediaQuery',
        'foundation.util.motion': '../vendor/foundation-sites/js/foundation.util.motion',
        'foundation.util.timerAndImageLoader': '../vendor/foundation-sites/js/foundation.util.timerAndImageLoader',
        'foundation.util.touch': '../vendor/foundation-sites/js/foundation.util.touch',
        'foundation.util.triggers': '../vendor/foundation-sites/js/foundation.util.triggers',

        'requirejs': '../vendor/requirejs/require',

        'slick': '../vendor/slick-carousel/slick/slick'
    },
    shim: {
        'foundation': {
            deps: [
                'jquery'
            ],
            exports: 'Foundation'
        },
        'foundation.util.box': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.keyboard': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.mediaQuery': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.motion': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.timerAndImageLoader': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.touch': {
            deps: [
                'foundation'
            ],
        },
        'foundation.util.triggers': {
            deps: [
                'foundation'
            ],
        },
        'foundation.equalizer': {
            deps: [
                'foundation',
                'foundation.util.mediaQuery',
                'foundation.util.timerAndImageLoader'
            ],
        },
        'slick': {
            deps: [
                'jquery'
            ],
            exports: 'Slick'
        },
        'ga': {
            exports: '__ga__'
        },
    }
});
