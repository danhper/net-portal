# Test helper
define([
    'handlebars'
], (Handlebars) ->
    toUpper = (text) ->
        text.toUpperCase()
    Handlebars.registerHelper('toUpper', toUpper)
    toUpper
)
