define([
    'module',
    'jquery',
    'modernizr',
    'foundation.dropdown',
    'foundation.equalizer',
    'foundation.orbit',
], function(module, $) {
    'use strict';

    $(document).ready(function() {
        // loads foundation
        $(document).foundation();
    });

    return module;
});
