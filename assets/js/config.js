//The build will inline common dependencies into this file.
//For any third party dependencies, like jQuery, place them in the lib folder.
//Configure loading modules from the lib directory,
//except for "app" ones, which are in a sibling
//directory.
requirejs.config({
    baseUrl: "/static/js",
    urlArgs: "bust=" + (new Date()).getTime(),
    paths: {
        "jquery": "../vendor/jquery/dist/jquery",

        // Foundation
        "foundation": "../vendor/foundation-sites/js/foundation.core",
        "foundation.dropdown": "../vendor/foundation-sites/js/foundation.dropdown",
        "foundation.equalizer": "../vendor/foundation-sites/js/foundation.equalizer",
        "foundation.orbit": "../vendor/foundation-sites/js/foundation.orbit",
        "foundation.util.box": "../vendor/foundation-sites/js/foundation.util.box",
        "foundation.util.keyboard": "../vendor/foundation-sites/js/foundation.util.keyboard",
        "foundation.util.mediaQuery": "../vendor/foundation-sites/js/foundation.util.mediaQuery",
        "foundation.util.motion": "../vendor/foundation-sites/js/foundation.util.motion",
        "foundation.util.timerAndImageLoader": "../vendor/foundation-sites/js/foundation.util.timerAndImageLoader",
        "foundation.util.touch": "../vendor/foundation-sites/js/foundation.util.touch",

        "modernizr": "../vendor/modernizr/modernizr",

        "requirejs": "../vendor/requirejs/require",

        "twitter": "widgets"
    },
    shim: {
        "foundation": {
            deps: [
                "jquery",
                "modernizr"
            ],
            exports: "Foundation"
        },
        "foundation.util.box": {
            deps: [
                "foundation"
            ],
        },
        "foundation.util.keyboard": {
            deps: [
                "foundation"
            ],
        },
        "foundation.util.mediaQuery": {
            deps: [
                "foundation"
            ],
        },
        "foundation.util.motion": {
            deps: [
                "foundation"
            ],
        },
        "foundation.util.timerAndImageLoader": {
            deps: [
                "foundation"
            ],
        },
        "foundation.util.touch": {
            deps: [
                "foundation"
            ],
        },
        "foundation.dropdown": {
            deps: [
                "foundation",
                "foundation.util.box",
                "foundation.util.keyboard"
            ],
        },
        "foundation.equalizer": {
            deps: [
                "foundation",
                "foundation.util.mediaQuery"
            ],
        },
        "foundation.orbit": {
            deps: [
                "foundation",
                "foundation.util.keyboard",
                "foundation.util.motion",
                "foundation.util.timerAndImageLoader",
                "foundation.util.touch"
            ],
        },
        "modernizr": {
            exports: "Modernizr"
        },
        "twitter": {
            deps: [
                "jquery",
                "modernizr"
            ]
        },
        "ga": {
            exports: "__ga__"
        },
    },
    deps: [
        "main"
    ]
});
