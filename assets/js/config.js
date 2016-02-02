//The build will inline common dependencies into this file.
//For any third party dependencies, like jQuery, place them in the lib folder.
//Configure loading modules from the lib directory,
//except for 'app' ones, which are in a sibling
//directory.
requirejs.config({
    baseUrl: "/static/js",
    urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        "jquery": "../vendor/jquery/dist/jquery.min",

        'foundation': '../vendor/foundation-sites/dist/foundation.min',

        "modernizr": "../vendor/modernizr/modernizr",

        "twitter": "//platform.twitter.com/widgets"
    },
    shim: {
        'modernizr': {
            exports: 'Modernizr'
        },
        /* Foundation */
        'foundation': {
            deps: [
                'jquery',
                'modernizr'
            ],
            exports: 'Foundation'
        },
        'ga': {
            exports: '__ga__'
        }
    },
    deps: [
        'main'
    ]
});
